"""Robustness checks for A1/A2/A4 surprising results.

R1: A2 EMA20 touch # — different forward windows (6, 24, 48 bars)
R2: A4 ATR z — abs forward return (directional strength), not just range
R3: A1 EMA alignment — different forward windows (1, 12, 24 bars)

Goal: confirm REVERSE/NOGO findings are robust, not measurement artifact.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators
from _lib.weighting import get_all_weights, weighted_mean
from _lib.stats import cohen_d, hit_rate

OUT_DIR = Path(__file__).parent / "results" / "R_robustness"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42


def run_R1_ema20_touch_windows(df: pd.DataFrame):
    """A2 robustness: 1st vs 4th+ touch hit rate across forward windows."""
    from A2_ema20_touch import detect_ema20_touches
    from _lib.path_sim import forward_mfe_mae

    print("\n[R1] EMA20 touch # × forward window")
    touches = detect_ema20_touches(df)
    print(f"  N total touches: {len(touches):,}")

    out = {}
    for fwd_bars in [6, 12, 24, 48]:
        sim = forward_mfe_mae(df, touches["touch_idx"].values, n_bars=fwd_bars, direction="long")
        sim = sim.reset_index(drop=True)
        t = touches.reset_index(drop=True).copy()
        t["mfe_atr"] = sim["mfe_price"].values / t["atr_at_touch"].values
        t = t.dropna(subset=["mfe_atr"])

        def bin_touch(n):
            if n == 1: return "1st"
            if n == 2: return "2nd"
            if n == 3: return "3rd"
            return "4th+"
        t["bin"] = t["touch_num"].apply(bin_touch)

        weights_all = get_all_weights(pd.DatetimeIndex(t["datetime"].values))
        h2y = weights_all["w_h2y"]
        l2y = weights_all["last_2y"]

        sub1 = t[t["bin"] == "1st"]
        sub4 = t[t["bin"] == "4th+"]
        sub1_idx = t.index.get_indexer(sub1.index)
        sub4_idx = t.index.get_indexer(sub4.index)

        hr_1st_h2y = hit_rate(sub1["mfe_atr"].values, h2y[sub1_idx], 1.0, ">=")
        hr_4th_h2y = hit_rate(sub4["mfe_atr"].values, h2y[sub4_idx], 1.0, ">=")
        hr_1st_l2y = hit_rate(sub1["mfe_atr"].values, l2y[sub1_idx], 1.0, ">=")
        hr_4th_l2y = hit_rate(sub4["mfe_atr"].values, l2y[sub4_idx], 1.0, ">=")

        delta_h2y = (hr_1st_h2y - hr_4th_h2y) * 100
        delta_l2y = (hr_1st_l2y - hr_4th_l2y) * 100
        out[f"fwd_{fwd_bars}"] = {
            "hr_1st_h2y": hr_1st_h2y, "hr_4th_h2y": hr_4th_h2y, "delta_h2y_pp": delta_h2y,
            "hr_1st_l2y": hr_1st_l2y, "hr_4th_l2y": hr_4th_l2y, "delta_l2y_pp": delta_l2y,
        }
        print(f"  fwd={fwd_bars:>3d}b: 1st={hr_1st_h2y*100:5.2f}% 4th+={hr_4th_h2y*100:5.2f}% Δ_h2y={delta_h2y:+5.2f}pp, Δ_l2y={delta_l2y:+5.2f}pp")
    return out


def run_R2_atr_z_directional(df: pd.DataFrame):
    """A4 robustness: forward |return|/ATR (directional strength, not range)."""
    print("\n[R2] ATR z × forward |return|/ATR")

    # ATR z 60-day
    atr_lookback = 60 * 24 * 12
    df["atr_mean60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).mean()
    df["atr_std60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).std()
    df["atr_z"] = (df["atr14"] - df["atr_mean60d"]) / df["atr_std60d"]
    df = df.dropna(subset=["atr_z"]).copy()

    out = {}
    for fwd_bars in [6, 12, 24, 48]:
        df["fwd_ret"] = df["close"].shift(-fwd_bars) - df["close"]
        df["fwd_abs_ret_atr"] = df["fwd_ret"].abs() / df["atr14"]
        df["fwd_signed_ret_atr"] = df["fwd_ret"] / df["atr14"]
        d = df.dropna(subset=["fwd_abs_ret_atr"])

        rng = np.random.default_rng(SEED)
        if len(d) > 30000:
            idx = rng.choice(len(d), size=30000, replace=False)
            idx.sort()
            sample = d.iloc[idx]
        else:
            sample = d

        def z_bin(z):
            if z < -0.5: return "low (z<-0.5)"
            if z < +0.5: return "base (-0.5..+0.5)"
            if z < +1.0: return "mid (+0.5..+1)"
            return "high (z>=+1)"
        sample = sample.copy()
        sample["bin"] = sample["atr_z"].apply(z_bin)

        weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
        h2y = weights_all["w_h2y"]

        results = {}
        for b in ["low (z<-0.5)", "base (-0.5..+0.5)", "mid (+0.5..+1)", "high (z>=+1)"]:
            sub = sample[sample["bin"] == b]
            if len(sub) < 100:
                continue
            sub_idx = sample.index.get_indexer(sub.index)
            mu_abs = weighted_mean(sub["fwd_abs_ret_atr"].values, h2y[sub_idx])
            mu_signed = weighted_mean(sub["fwd_signed_ret_atr"].values, h2y[sub_idx])
            results[b] = {"n": int(len(sub)), "mu_abs": mu_abs, "mu_signed": mu_signed}

        out[f"fwd_{fwd_bars}"] = results
        print(f"  fwd={fwd_bars}b:")
        for b, r in results.items():
            print(f"    {b:22s} N={r['n']:>5d} |ret|/ATR={r['mu_abs']:.3f} signed_ret/ATR={r['mu_signed']:+.4f}")

    return out


def run_R3_ema_alignment_windows(df: pd.DataFrame):
    """A1 robustness: EMA alignment effect on multiple forward windows."""
    print("\n[R3] EMA alignment × forward window")

    bullish = (df["ema20"] > df["ema50"]) & (df["ema50"] > df["ema200"])
    bearish = (df["ema20"] < df["ema50"]) & (df["ema50"] < df["ema200"])
    df["align"] = "혼"
    df.loc[bullish, "align"] = "정"
    df.loc[bearish, "align"] = "역"

    out = {}
    for fwd_bars in [1, 3, 5, 12, 24, 48]:
        forward_close = df["close"].shift(-fwd_bars)
        df["fwd_ret_atr"] = (forward_close - df["close"]) / df["atr14"]
        d = df.dropna(subset=["fwd_ret_atr"])

        rng = np.random.default_rng(SEED)
        if len(d) > 30000:
            idx = rng.choice(len(d), size=30000, replace=False)
            idx.sort()
            sample = d.iloc[idx]
        else:
            sample = d

        weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
        h2y = weights_all["w_h2y"]
        l2y = weights_all["last_2y"]

        b_mask = (sample["align"] == "정").values
        r_mask = (sample["align"] == "역").values
        f = sample["fwd_ret_atr"].values

        if r_mask.sum() < 30 or b_mask.sum() < 30:
            continue

        d_h2y = cohen_d(f[b_mask], f[r_mask], h2y[b_mask], h2y[r_mask])
        d_l2y = cohen_d(f[b_mask], f[r_mask], l2y[b_mask], l2y[r_mask])
        mu_b_h2y = weighted_mean(f[b_mask], h2y[b_mask])
        mu_r_h2y = weighted_mean(f[r_mask], h2y[r_mask])
        out[f"fwd_{fwd_bars}"] = {
            "d_h2y": d_h2y, "d_l2y": d_l2y,
            "mu_정_h2y": mu_b_h2y, "mu_역_h2y": mu_r_h2y,
        }
        print(f"  fwd={fwd_bars:>3d}b: d_h2y={d_h2y:+.4f}, d_l2y={d_l2y:+.4f}, mu_정={mu_b_h2y:+.3f}, mu_역={mu_r_h2y:+.3f}")

    return out


def main():
    print("[R] Loading NQ 5m + indicators...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df = df.dropna(subset=["ema20", "ema50", "ema200", "atr14"])

    results = {}
    results["R1_ema20_touch"] = run_R1_ema20_touch_windows(df.set_index(df.index))
    results["R2_atr_z_directional"] = run_R2_atr_z_directional(df.copy())
    results["R3_ema_alignment_windows"] = run_R3_ema_alignment_windows(df.copy())

    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[R] Saved → {OUT_DIR / 'results.json'}")


if __name__ == "__main__":
    main()
