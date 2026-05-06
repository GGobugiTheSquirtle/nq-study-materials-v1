"""A4: ATR z-score forward range/return distribution (W9)

H0: ATR z bin (-2/-1/0/+1/+2/+3) 별 forward 12-bar range/return 동일
H1: z >= +1.0 → forward range >= 130% × baseline (z=0), w_h2y

Method:
  - ATR z = (current ATR - 60-day rolling ATR mean) / std
  - Bin every bar by z bucket
  - For each bar, compute forward 12-bar (high-low) range / current ATR
  - Compare distributions
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators
from _lib.weighting import get_all_weights, weighted_mean
from _lib.stats import cohen_d, interpret_d, hit_rate

OUT_DIR = Path(__file__).parent / "results" / "A4_atr_zscore"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FORWARD_BARS = 12
SAMPLE_N = 30000
SEED = 42
ATR_LOOKBACK_BARS = 60 * 24 * 12   # 60 days × 24h × 12 bars/h = 17,280 bars (5m)


def main():
    print("[A4] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df = df.dropna(subset=["atr14"]).copy()

    print("[A4] Computing ATR z-score (60-day rolling)...")
    # Use rolling mean/std of ATR over 60 days
    df["atr_mean60d"] = df["atr14"].rolling(window=ATR_LOOKBACK_BARS, min_periods=1000).mean()
    df["atr_std60d"] = df["atr14"].rolling(window=ATR_LOOKBACK_BARS, min_periods=1000).std()
    df["atr_z"] = (df["atr14"] - df["atr_mean60d"]) / df["atr_std60d"]
    df = df.dropna(subset=["atr_z"]).copy()
    print(f"  bars after warmup: {len(df):,}")

    # Forward 12-bar range
    fwd_high = df["high"].rolling(window=FORWARD_BARS).max().shift(-FORWARD_BARS)
    fwd_low = df["low"].rolling(window=FORWARD_BARS).min().shift(-FORWARD_BARS)
    df["fwd_range"] = fwd_high - fwd_low
    df["fwd_range_atr"] = df["fwd_range"] / df["atr14"]
    df["fwd_ret_atr"] = (df["close"].shift(-FORWARD_BARS) - df["close"]) / df["atr14"]
    df = df.dropna(subset=["fwd_range_atr", "fwd_ret_atr"])

    # Sample
    rng = np.random.default_rng(SEED)
    if len(df) > SAMPLE_N:
        idx = rng.choice(len(df), size=SAMPLE_N, replace=False)
        idx.sort()
        sample = df.iloc[idx]
    else:
        sample = df

    print(f"[A4] sample N={len(sample):,}")
    print(f"  z range: [{sample['atr_z'].min():.2f}, {sample['atr_z'].max():.2f}]")
    print(f"  z mean: {sample['atr_z'].mean():.3f}, std: {sample['atr_z'].std():.3f}")

    def z_bin(z):
        if z < -1.0: return "z<-1"
        if z < -0.5: return "-1<=z<-0.5"
        if z < 0.5: return "-0.5<=z<+0.5"
        if z < 1.0: return "+0.5<=z<+1.0"
        if z < 2.0: return "+1.0<=z<+2.0"
        return "z>=+2.0"

    sample = sample.copy()
    sample["bin"] = sample["atr_z"].apply(z_bin)

    bins_order = ["z<-1", "-1<=z<-0.5", "-0.5<=z<+0.5", "+0.5<=z<+1.0", "+1.0<=z<+2.0", "z>=+2.0"]

    weights_all = get_all_weights(pd.DatetimeIndex(sample.index))

    print(f"\n[A4] === Forward range/ATR by z bin × scheme ===")
    print(f"{'z bin':16s} {'N':>7s}", end=" ")
    for scheme in weights_all.keys():
        print(f"{scheme:>10s}", end=" ")
    print()

    results = {
        "hypothesis": "ATR z-score bin 별 forward 12-bar range / current ATR ratio",
        "n_sample": int(len(sample)),
        "data_range": [str(sample.index[0]), str(sample.index[-1])],
        "by_bin_by_scheme": {},
    }

    for b in bins_order:
        sub = sample[sample["bin"] == b]
        if len(sub) == 0:
            continue
        sub_idx = sample.index.get_indexer(sub.index)
        n_b = len(sub)
        results["by_bin_by_scheme"][b] = {"n": n_b}
        print(f"{b:16s} {n_b:>7d}", end=" ")
        for scheme, w in weights_all.items():
            w_sub = w[sub_idx]
            mu = weighted_mean(sub["fwd_range_atr"].values, w_sub)
            results["by_bin_by_scheme"][b][scheme] = mu
            print(f"{mu:>9.3f}", end="  ")
        print()

    # Compare z>=1.0 vs z near 0 (-0.5 ~ +0.5)
    high_mask = sample["bin"].isin(["+1.0<=z<+2.0", "z>=+2.0"])
    base_mask = sample["bin"] == "-0.5<=z<+0.5"
    high = sample[high_mask]
    base = sample[base_mask]
    high_idx = sample.index.get_indexer(high.index)
    base_idx = sample.index.get_indexer(base.index)

    print(f"\n[A4] === High momentum (z>=+1) vs Baseline (-0.5<=z<+0.5) ===")
    print(f"{'Scheme':10s} {'high mu':>10s} {'base mu':>10s} {'ratio':>10s} {'delta':>10s}")
    ratio_by_scheme = {}
    delta_by_scheme = {}
    for scheme, w in weights_all.items():
        mu_high = weighted_mean(high["fwd_range_atr"].values, w[high_idx])
        mu_base = weighted_mean(base["fwd_range_atr"].values, w[base_idx])
        ratio = mu_high / mu_base if mu_base > 0 else 0
        delta = mu_high - mu_base
        ratio_by_scheme[scheme] = ratio
        delta_by_scheme[scheme] = delta
        print(f"{scheme:10s} {mu_high:>10.3f} {mu_base:>10.3f} {ratio:>10.3f} {delta:>+10.3f}")

    results["high_vs_base"] = {"ratio": ratio_by_scheme, "delta": delta_by_scheme}

    # Monotonicity check
    print(f"\n[A4] === Monotonicity check (mu by bin, w_h2y) ===")
    h2y = weights_all["w_h2y"]
    mus = []
    for b in bins_order:
        sub = sample[sample["bin"] == b]
        if len(sub) == 0:
            mus.append(None)
            continue
        sub_idx = sample.index.get_indexer(sub.index)
        mu = weighted_mean(sub["fwd_range_atr"].values, h2y[sub_idx])
        mus.append(mu)
        print(f"  {b:16s}: {mu:.3f}")
    monotonic = all(mus[i] is None or mus[i+1] is None or mus[i+1] >= mus[i] for i in range(len(mus)-1))
    results["monotonic_h2y"] = monotonic
    print(f"  Monotonic increasing: {monotonic}")

    # Judgment
    ratio_h2y = ratio_by_scheme["w_h2y"]
    ratio_l2y = ratio_by_scheme["last_2y"]
    if ratio_h2y >= 1.30 and ratio_l2y >= 1.30:
        judgment = "GO"
    elif ratio_h2y >= 1.30 or ratio_l2y >= 1.30:
        judgment = "PARTIAL"
    else:
        judgment = "NOGO"
    results["judgment"] = judgment

    print(f"\n[A4] PRIMARY: high/base ratio (w_h2y) = {ratio_h2y:.3f}")
    print(f"[A4] === JUDGMENT: {judgment} ===")

    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[A4] Saved → {OUT_DIR / 'results.json'}")
    return results


if __name__ == "__main__":
    main()
