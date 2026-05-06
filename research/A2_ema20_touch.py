"""A2: EMA20 touch # 별 hit rate (W6)

H0: 1st/2nd/3rd/4th+ touch hit rate (forward MFE 1×ATR 도달) 동일
H1: 1st touch hit rate >= 4th+ touch hit rate + 10pp, w_h2y

Touch event 정의:
  - 정배열 (ema20 > ema50 > ema200) 구간만 (uptrend confirm)
  - Price > EMA20 → Price ≤ EMA20 (close 기준) 진입 = touch event
  - 같은 swing 내 연속 touch 카운트 (price 가 다시 EMA20 위로 올라가야 swing reset)

Forward measure:
  - MFE 도달률 (1×ATR up from touch close)
  - within next 12 bars (= 1 hour)
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators, regime_label
from _lib.weighting import get_all_weights, weighted_mean, effective_n
from _lib.stats import cohen_d, judge_phase_a, interpret_d, hit_rate
from _lib.path_sim import forward_mfe_mae

OUT_DIR = Path(__file__).parent / "results" / "A2_ema20_touch"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FORWARD_BARS = 12     # 1 hour
MFE_THRESHOLD_ATR = 1.0
SEED = 42


def detect_ema20_touches(df: pd.DataFrame) -> pd.DataFrame:
    """Detect EMA20 touch events in 정배열 uptrend.

    A 'touch' = bar where:
      - 정배열 (ema20 > ema50 > ema200)
      - prev close > ema20 AND current close <= ema20
      - touch # = consecutive count, resets when close > ema20 + 0.5×ATR (clear above)

    Returns DataFrame with touch_idx (int position), touch_num (1, 2, 3, ...).
    """
    close = df["close"].values
    ema20 = df["ema20"].values
    ema50 = df["ema50"].values
    ema200 = df["ema200"].values
    atr14 = df["atr14"].values
    n = len(df)

    bullish = (ema20 > ema50) & (ema50 > ema200)

    touches = []
    cur_touch_num = 0
    above_clear_count = 0  # bars consecutively clear above EMA20

    for i in range(1, n):
        if not bullish[i]:
            cur_touch_num = 0
            above_clear_count = 0
            continue
        # Reset condition: clear above ema20 by 0.5×ATR for 3+ bars
        if close[i] > ema20[i] + 0.5 * atr14[i]:
            above_clear_count += 1
            if above_clear_count >= 3:
                cur_touch_num = 0  # new swing starts
        else:
            above_clear_count = 0
        # Touch event: prev close > ema20, current close <= ema20
        if close[i - 1] > ema20[i - 1] and close[i] <= ema20[i]:
            cur_touch_num += 1
            touches.append({"touch_idx": i, "touch_num": cur_touch_num,
                            "datetime": df.index[i],
                            "close_at_touch": close[i],
                            "atr_at_touch": atr14[i]})

    return pd.DataFrame(touches)


def main():
    print("[A2] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df["regime"] = regime_label(df)
    df = df.dropna(subset=["ema20", "ema50", "ema200", "atr14"]).reset_index()

    print("[A2] Detecting EMA20 touches in uptrend...")
    touches = detect_ema20_touches(df.set_index("datetime"))
    print(f"  total touches: {len(touches):,}")
    print(f"  touch_num distribution:")
    print(touches["touch_num"].value_counts().sort_index().head(10).to_string())

    # Path-sim forward MFE
    df_idx = df.set_index("datetime")
    entry_idx = touches["touch_idx"].values
    print(f"[A2] Path-sim forward MFE for {len(entry_idx):,} touches...")
    sim = forward_mfe_mae(df_idx, entry_idx, n_bars=FORWARD_BARS, direction="long")
    sim = sim.reset_index(drop=True)
    touches = touches.reset_index(drop=True)
    touches["mfe_atr"] = sim["mfe_price"].values / touches["atr_at_touch"].values
    touches["mae_atr"] = sim["mae_price"].values / touches["atr_at_touch"].values
    touches = touches.dropna(subset=["mfe_atr"])
    print(f"  valid (with forward window): {len(touches):,}")

    # Bin touch numbers
    def bin_touch(n):
        if n == 1: return "1st"
        if n == 2: return "2nd"
        if n == 3: return "3rd"
        return "4th+"
    touches["bin"] = touches["touch_num"].apply(bin_touch)

    # Weights
    weights_all = get_all_weights(pd.DatetimeIndex(touches["datetime"].values))
    mfe = touches["mfe_atr"].values

    # Hit rate by bin × scheme
    print(f"\n[A2] === Hit rate (MFE >= {MFE_THRESHOLD_ATR}×ATR) by bin × scheme ===")
    print(f"{'Bin':6s} {'N':>7s}", end=" ")
    for scheme in weights_all.keys():
        print(f"{scheme:>10s}", end=" ")
    print()

    results = {
        "hypothesis": f"EMA20 touch # 별 forward MFE >= {MFE_THRESHOLD_ATR}×ATR within {FORWARD_BARS} bars hit rate",
        "n_touches": int(len(touches)),
        "data_range": [str(touches["datetime"].iloc[0]), str(touches["datetime"].iloc[-1])],
        "by_bin_by_scheme": {},
    }

    bin_data = {}
    for b in ["1st", "2nd", "3rd", "4th+"]:
        sub = touches[touches["bin"] == b]
        bin_data[b] = sub
        sub_idx = touches.index.get_indexer(sub.index)
        n_b = len(sub)
        results["by_bin_by_scheme"][b] = {"n": n_b}
        print(f"{b:6s} {n_b:>7d}", end=" ")
        for scheme, w in weights_all.items():
            w_sub = w[sub_idx]
            hr = hit_rate(sub["mfe_atr"].values, w_sub, MFE_THRESHOLD_ATR, ">=")
            results["by_bin_by_scheme"][b][scheme] = hr
            print(f"{hr*100:>9.2f}%", end=" ")
        print()

    # Cohen d 1st vs 4th+ for each scheme
    print(f"\n[A2] === d (1st vs 4th+) by scheme ===")
    sub1 = touches[touches["bin"] == "1st"]
    sub4 = touches[touches["bin"] == "4th+"]
    sub1_idx = touches.index.get_indexer(sub1.index)
    sub4_idx = touches.index.get_indexer(sub4.index)

    d_by_scheme = {}
    for scheme, w in weights_all.items():
        w1 = w[sub1_idx]
        w4 = w[sub4_idx]
        # Use binary hit indicator for d (effect on hit rate)
        h1 = (sub1["mfe_atr"].values >= MFE_THRESHOLD_ATR).astype(float)
        h4 = (sub4["mfe_atr"].values >= MFE_THRESHOLD_ATR).astype(float)
        d = cohen_d(h1, h4, w1, w4)
        d_by_scheme[scheme] = d
        delta_pp = (weighted_mean(h1, w1) - weighted_mean(h4, w4)) * 100
        print(f"  {scheme:10s}: d={d:+.4f} ({interpret_d(d)}), delta hit rate = {delta_pp:+.2f}pp")

    results["d_1st_vs_4th_by_scheme"] = d_by_scheme

    # Judgment based on hit rate delta (not Cohen d for binary)
    h_1st_h2y = results["by_bin_by_scheme"]["1st"]["w_h2y"]
    h_4th_h2y = results["by_bin_by_scheme"]["4th+"]["w_h2y"]
    delta_pp_h2y = (h_1st_h2y - h_4th_h2y) * 100

    if delta_pp_h2y >= 10:
        judgment = "GO"
    elif delta_pp_h2y >= 5:
        judgment = "PARTIAL"
    elif delta_pp_h2y < 0:
        judgment = "REVERSE"   # 4th+ better than 1st (unexpected)
    else:
        judgment = "NOGO"
    results["judgment"] = judgment
    results["delta_pp_h2y"] = delta_pp_h2y

    print(f"\n[A2] PRIMARY: 1st vs 4th+ hit rate delta (w_h2y) = {delta_pp_h2y:+.2f}pp")
    print(f"[A2] === JUDGMENT: {judgment} ===")

    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[A2] Saved → {OUT_DIR / 'results.json'}")
    return results


if __name__ == "__main__":
    main()
