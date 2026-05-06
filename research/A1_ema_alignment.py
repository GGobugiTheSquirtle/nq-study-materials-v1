"""A1: EMA 정배열 = LONG bias 효과 (W2)

H0: 진입 시점 EMA 배열 (정/혼/역) 별 forward 5-bar return distribution 동일
H1: 정배열 진입 forward return 평균 > 역배열, w_h2y Cohen's d ≥ 0.15

Method:
  - Sample N=10,000 random bars (with replacement removed) across 10y NQ 5m
  - At each bar t, classify alignment based on (ema20[t], ema50[t], ema200[t]):
    정 = ema20 > ema50 > ema200
    역 = ema20 < ema50 < ema200
    혼 = else
  - forward_ret = (close[t+5] - close[t]) / atr14[t]   # ATR-normalized
  - For each pair (정 vs 역, 정 vs 혼, 역 vs 혼) compute weighted Cohen's d under 5 schemes
  - Regime breakdown
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators, regime_label
from _lib.weighting import get_all_weights, weighted_mean, weighted_std, effective_n
from _lib.stats import cohen_d, judge_phase_a, interpret_d, bootstrap_ci

OUT_DIR = Path(__file__).parent / "results" / "A1_ema_alignment"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FORWARD_BARS = 5
SAMPLE_N = 30000
SEED = 42


def classify_alignment(ema20, ema50, ema200):
    out = np.full(len(ema20), "혼", dtype=object)
    bullish = (ema20 > ema50) & (ema50 > ema200)
    bearish = (ema20 < ema50) & (ema50 < ema200)
    out[bullish] = "정"
    out[bearish] = "역"
    return out


def main():
    print("[A1] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df["regime"] = regime_label(df)

    # Drop NaN (early bars without ema200)
    df = df.dropna(subset=["ema20", "ema50", "ema200", "atr14"]).copy()
    n_total = len(df)
    print(f"  bars after warmup: {n_total:,}")

    # Forward return ATR-normalized
    forward_close = df["close"].shift(-FORWARD_BARS)
    df["fwd_ret_atr"] = (forward_close - df["close"]) / df["atr14"]
    df = df.dropna(subset=["fwd_ret_atr"])

    # Alignment label
    df["align"] = classify_alignment(df["ema20"].values, df["ema50"].values, df["ema200"].values)

    # Sample
    rng = np.random.default_rng(SEED)
    if len(df) > SAMPLE_N:
        sample_idx = rng.choice(len(df), size=SAMPLE_N, replace=False)
        sample_idx.sort()
        sample = df.iloc[sample_idx]
    else:
        sample = df

    print(f"  sample size: {len(sample):,}")
    print(f"  align distribution: {sample['align'].value_counts().to_dict()}")
    print(f"  regime distribution: {sample['regime'].value_counts().to_dict()}")

    # ---------- Compute Cohen's d under each weighting ----------
    weights_all = get_all_weights(sample.index)
    fwd = sample["fwd_ret_atr"].values
    align = sample["align"].values

    bullish_mask = align == "정"
    bearish_mask = align == "역"
    mixed_mask = align == "혼"

    results = {
        "hypothesis": "EMA alignment (정/역/혼) 별 forward 5-bar ATR-normalized return 차이",
        "sample_n": int(len(sample)),
        "data_range": [str(df.index[0]), str(df.index[-1])],
        "forward_bars": FORWARD_BARS,
        "by_weighting": {},
        "by_regime": {},
    }

    print("\n[A1] === By Weighting ===")
    print(f"{'Scheme':10s} {'mu_정':>8s} {'mu_혼':>8s} {'mu_역':>8s} {'d(정vs역)':>12s} {'d(정vs혼)':>12s}")
    for scheme, w in weights_all.items():
        w_b = w[bullish_mask]
        w_m = w[mixed_mask]
        w_r = w[bearish_mask]
        f_b = fwd[bullish_mask]
        f_m = fwd[mixed_mask]
        f_r = fwd[bearish_mask]
        if len(f_b) == 0 or len(f_r) == 0 or len(f_m) == 0:
            continue
        mu_b = weighted_mean(f_b, w_b)
        mu_m = weighted_mean(f_m, w_m)
        mu_r = weighted_mean(f_r, w_r)
        d_br = cohen_d(f_b, f_r, w_b, w_r)
        d_bm = cohen_d(f_b, f_m, w_b, w_m)
        n_eff = {"bull": effective_n(w_b), "mix": effective_n(w_m), "bear": effective_n(w_r)}
        results["by_weighting"][scheme] = {
            "mu_정": mu_b, "mu_혼": mu_m, "mu_역": mu_r,
            "cohen_d_정vs역": d_br,
            "cohen_d_정vs혼": d_bm,
            "n_eff": n_eff,
        }
        print(f"{scheme:10s} {mu_b:>+8.4f} {mu_m:>+8.4f} {mu_r:>+8.4f} {d_br:>+12.4f} {d_bm:>+12.4f}")

    # Bootstrap CI for primary metric (정 vs 역, w_h2y)
    print("\n[A1] Bootstrap CI for d(정 vs 역) primary scheme w_h2y ...")
    w_h2y = weights_all["w_h2y"]
    rng = np.random.default_rng(SEED + 1)
    n_boot = 500
    boot_d = np.empty(n_boot)
    for i in range(n_boot):
        idx_b = rng.choice(np.where(bullish_mask)[0], size=int(min(len(np.where(bullish_mask)[0]), 5000)), replace=True,
                           p=w_h2y[bullish_mask] / w_h2y[bullish_mask].sum())
        idx_r = rng.choice(np.where(bearish_mask)[0], size=int(min(len(np.where(bearish_mask)[0]), 5000)), replace=True,
                           p=w_h2y[bearish_mask] / w_h2y[bearish_mask].sum())
        boot_d[i] = cohen_d(fwd[idx_b], fwd[idx_r])
    ci_lo, ci_hi = float(np.quantile(boot_d, 0.025)), float(np.quantile(boot_d, 0.975))
    print(f"  d(정 vs 역) w_h2y CI95 = [{ci_lo:+.4f}, {ci_hi:+.4f}]")
    results["bootstrap_ci_d_정vs역_h2y"] = {"ci_low": ci_lo, "ci_high": ci_hi, "n_boot": n_boot}

    # ---------- By Regime ----------
    print("\n[A1] === By Regime (w_h2y) ===")
    print(f"{'Regime':8s} {'N':>8s} {'mu_정':>8s} {'mu_역':>8s} {'d(정vs역)':>12s}")
    for reg in ["BULL", "BEAR", "CHOP"]:
        sub = sample[sample["regime"] == reg]
        if len(sub) < 200:
            print(f"  {reg}: insufficient (N={len(sub)})")
            continue
        sub_idx = sample.index.get_indexer(sub.index)
        w_sub = w_h2y[sub_idx]
        f_sub = fwd[sub_idx]
        align_sub = align[sub_idx]
        b = align_sub == "정"
        r = align_sub == "역"
        if b.sum() < 30 or r.sum() < 30:
            print(f"  {reg}: insufficient sub-group (N_정={b.sum()}, N_역={r.sum()})")
            continue
        mu_b = weighted_mean(f_sub[b], w_sub[b])
        mu_r = weighted_mean(f_sub[r], w_sub[r])
        d_br = cohen_d(f_sub[b], f_sub[r], w_sub[b], w_sub[r])
        print(f"{reg:8s} {len(sub):>8d} {mu_b:>+8.4f} {mu_r:>+8.4f} {d_br:>+12.4f}")
        results["by_regime"][reg] = {"n": int(len(sub)), "mu_정": mu_b, "mu_역": mu_r, "cohen_d_정vs역": d_br}

    # ---------- Judgment ----------
    d_by_scheme = {k: v["cohen_d_정vs역"] for k, v in results["by_weighting"].items()}
    judgment = judge_phase_a(d_by_scheme, threshold=0.15)
    results["judgment"] = judgment
    results["d_by_scheme"] = d_by_scheme
    print(f"\n[A1] PRIMARY: d(정 vs 역) by scheme = " +
          ", ".join(f"{k}={v:+.3f}" for k, v in d_by_scheme.items()))
    print(f"[A1] === JUDGMENT: {judgment} ===")
    print(f"[A1] interpretation w_h2y: d={d_by_scheme['w_h2y']:+.3f} ({interpret_d(d_by_scheme['w_h2y'])})")

    # Save
    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[A1] Saved → {OUT_DIR / 'results.json'}")

    return results


if __name__ == "__main__":
    main()
