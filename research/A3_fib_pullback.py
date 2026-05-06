"""A3: Fib 38.2-61.8 Pullback win rate (W8) ⭐⭐⭐ 사용자 핵심 약점 처방

H0: Pullback 진입 fib level (23.6 / 38.2 / 50 / 61.8 / 78.6 / 100+) 별 forward win rate 동일
H1: 38.2-61.8% level 의 forward MFE 1×ATR hit rate > 23.6% AND > 78.6%, w_h2y +5pp

Method:
  - 정배열 구간만 (uptrend confirm)
  - Swing high → swing low pullback (ZigZag-like)
  - At each pullback bar, compute fib retrace level relative to last swing leg
  - Bin by level, measure forward MFE 1×ATR hit rate within next 12 bars

Pullback detection (simplified):
  - Find swing highs (local max in N=20 bar window)
  - From each swing high, track pullback bars (close decreasing)
  - For each pullback bar in 정배열, compute retrace %
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators, regime_label
from _lib.weighting import get_all_weights, weighted_mean
from _lib.stats import cohen_d, interpret_d, hit_rate
from _lib.path_sim import forward_mfe_mae

OUT_DIR = Path(__file__).parent / "results" / "A3_fib_pullback"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FORWARD_BARS = 12
MFE_THRESHOLD_ATR = 1.0
SEED = 42
SWING_LOOKBACK = 20    # bars for local max detection
MIN_LEG_ATR = 1.5      # minimum leg size in ATR (filter noise)


def detect_pullbacks(df: pd.DataFrame) -> pd.DataFrame:
    """Detect pullback events in 정배열 uptrend.

    Logic:
      1. Identify swing highs (local max within ±SWING_LOOKBACK bars)
      2. For each swing high SH, track subsequent bars where close < SH
      3. The leg start = previous swing low (last close <= ema20 before SH)
      4. Retrace % = (SH - current_close) / (SH - leg_start)
      5. Only count bars where 정배열 + retrace 0~120%
    """
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    ema20 = df["ema20"].values
    ema50 = df["ema50"].values
    ema200 = df["ema200"].values
    atr14 = df["atr14"].values
    n = len(df)

    bullish = (ema20 > ema50) & (ema50 > ema200)

    # Find swing highs: high[i] > high[i-LB:i+LB]
    is_swing_high = np.zeros(n, dtype=bool)
    LB = SWING_LOOKBACK
    for i in range(LB, n - LB):
        if high[i] == high[i - LB:i + LB + 1].max():
            is_swing_high[i] = True

    # Iterate forward, tracking current swing high and leg-start
    pullbacks = []
    current_sh_idx = -1
    current_leg_start_idx = -1
    current_sh_price = None
    current_leg_start_price = None

    for i in range(LB, n):
        if not bullish[i]:
            current_sh_idx = -1
            continue

        # New swing high?
        if is_swing_high[i]:
            current_sh_idx = i
            current_sh_price = high[i]
            # Find leg start: walk back until close <= ema20 within last 100 bars
            for j in range(i - 1, max(i - 100, 0), -1):
                if close[j] <= ema20[j]:
                    current_leg_start_idx = j
                    current_leg_start_price = low[j]  # use low as leg low
                    break
            else:
                current_leg_start_idx = -1
            continue

        # Track pullback after swing high
        if current_sh_idx > 0 and current_leg_start_idx > 0 and i > current_sh_idx:
            leg_size = current_sh_price - current_leg_start_price
            if leg_size <= MIN_LEG_ATR * atr14[current_sh_idx]:
                continue
            retrace = (current_sh_price - close[i]) / leg_size
            if 0.05 < retrace < 1.5:    # only meaningful pullbacks
                pullbacks.append({
                    "idx": i,
                    "datetime": df.index[i],
                    "close": close[i],
                    "atr": atr14[i],
                    "retrace": retrace,
                    "sh_idx": current_sh_idx,
                    "leg_size": leg_size,
                    "leg_size_atr": leg_size / atr14[current_sh_idx],
                })
                # If close > swing high, swing breaks → reset
                if close[i] > current_sh_price:
                    current_sh_idx = -1

    return pd.DataFrame(pullbacks)


def fib_bin(retrace: float) -> str:
    if retrace < 0.236: return "<23.6%"
    if retrace < 0.382: return "23.6-38.2%"
    if retrace < 0.500: return "38.2-50%"
    if retrace < 0.618: return "50-61.8%"
    if retrace < 0.786: return "61.8-78.6%"
    if retrace < 1.000: return "78.6-100%"
    return ">100% (broken)"


def main():
    print("[A3] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df["regime"] = regime_label(df)
    df = df.dropna(subset=["ema20", "ema50", "ema200", "atr14"])

    print("[A3] Detecting pullback events in 정배열 uptrend...")
    pullbacks = detect_pullbacks(df)
    print(f"  total pullback bars: {len(pullbacks):,}")

    print("[A3] Path-sim forward MFE...")
    entry_idx = pullbacks["idx"].values
    sim = forward_mfe_mae(df, entry_idx, n_bars=FORWARD_BARS, direction="long")
    sim = sim.reset_index(drop=True)
    pullbacks = pullbacks.reset_index(drop=True)
    pullbacks["mfe_atr"] = sim["mfe_price"].values / pullbacks["atr"].values
    pullbacks["mae_atr"] = sim["mae_price"].values / pullbacks["atr"].values
    pullbacks = pullbacks.dropna(subset=["mfe_atr"])
    print(f"  valid: {len(pullbacks):,}")

    # Bin
    pullbacks["bin"] = pullbacks["retrace"].apply(fib_bin)
    print(f"  bin distribution:")
    print(pullbacks["bin"].value_counts().to_string())

    # Hit rate by bin × scheme
    weights_all = get_all_weights(pd.DatetimeIndex(pullbacks["datetime"].values))
    bins_order = ["<23.6%", "23.6-38.2%", "38.2-50%", "50-61.8%", "61.8-78.6%", "78.6-100%", ">100% (broken)"]

    results = {
        "hypothesis": f"Fib pullback level 별 forward MFE >= {MFE_THRESHOLD_ATR}×ATR within {FORWARD_BARS} bars hit rate",
        "n_pullbacks": int(len(pullbacks)),
        "data_range": [str(pullbacks["datetime"].iloc[0]), str(pullbacks["datetime"].iloc[-1])],
        "by_bin_by_scheme": {},
    }

    print(f"\n[A3] === Hit rate (MFE >= {MFE_THRESHOLD_ATR}×ATR) by bin × scheme ===")
    print(f"{'Bin':16s} {'N':>7s}", end=" ")
    for scheme in weights_all.keys():
        print(f"{scheme:>10s}", end=" ")
    print()

    for b in bins_order:
        sub = pullbacks[pullbacks["bin"] == b]
        if len(sub) == 0:
            continue
        sub_idx = pullbacks.index.get_indexer(sub.index)
        n_b = len(sub)
        results["by_bin_by_scheme"][b] = {"n": n_b}
        print(f"{b:16s} {n_b:>7d}", end=" ")
        for scheme, w in weights_all.items():
            w_sub = w[sub_idx]
            hr = hit_rate(sub["mfe_atr"].values, w_sub, MFE_THRESHOLD_ATR, ">=")
            results["by_bin_by_scheme"][b][scheme] = hr
            print(f"{hr*100:>9.2f}%", end=" ")
        print()

    # Compare 38.2-50 + 50-61.8 (sweet spot) vs <23.6 + 78.6+
    sweet_mask = pullbacks["bin"].isin(["38.2-50%", "50-61.8%"])
    extreme_mask = pullbacks["bin"].isin(["<23.6%", "78.6-100%", ">100% (broken)"])
    sweet = pullbacks[sweet_mask]
    extreme = pullbacks[extreme_mask]
    sweet_idx = pullbacks.index.get_indexer(sweet.index)
    extreme_idx = pullbacks.index.get_indexer(extreme.index)

    print(f"\n[A3] === Sweet spot (38.2-61.8%) vs Extreme (<23.6 + 78.6+) ===")
    print(f"{'Scheme':10s} {'sweet HR':>10s} {'extreme HR':>12s} {'delta_pp':>10s}")
    delta_by_scheme = {}
    for scheme, w in weights_all.items():
        hr_sweet = hit_rate(sweet["mfe_atr"].values, w[sweet_idx], MFE_THRESHOLD_ATR, ">=")
        hr_extr = hit_rate(extreme["mfe_atr"].values, w[extreme_idx], MFE_THRESHOLD_ATR, ">=")
        delta_pp = (hr_sweet - hr_extr) * 100
        delta_by_scheme[scheme] = delta_pp
        print(f"{scheme:10s} {hr_sweet*100:>9.2f}% {hr_extr*100:>11.2f}% {delta_pp:>+10.2f}pp")

    results["sweet_vs_extreme_delta_pp"] = delta_by_scheme

    # Judgment
    delta_h2y = delta_by_scheme["w_h2y"]
    delta_l2y = delta_by_scheme["last_2y"]
    if delta_h2y >= 5 and delta_l2y >= 5:
        judgment = "GO"
    elif delta_h2y >= 5 or delta_l2y >= 5:
        judgment = "PARTIAL"
    elif delta_h2y < 0 or delta_l2y < 0:
        judgment = "REVERSE"
    else:
        judgment = "NOGO"
    results["judgment"] = judgment
    results["delta_pp_h2y"] = delta_h2y

    print(f"\n[A3] PRIMARY: sweet vs extreme delta (w_h2y) = {delta_h2y:+.2f}pp")
    print(f"[A3] === JUDGMENT: {judgment} ===")

    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[A3] Saved → {OUT_DIR / 'results.json'}")
    return results


if __name__ == "__main__":
    main()
