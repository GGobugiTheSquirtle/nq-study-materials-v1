"""D6: Multi-factor confluence — best NQ 5m signal combinations.

Combines discovered single-factor signals:
  - KST hour bias (D1): KST 04 LONG / KST 19 LONG / KST 22 SHORT / KST 20-21 SHORT
  - Day of week (D5): Monday LONG / Tuesday SHORT
  - ATR z squeeze (D3): squeeze_12 → expansion
  - Strong body candle (D4): bull/bear continuation
  - Extreme past return (D2): continuation small effect

Test: 결합 시 effect size 가 단일 factor 합 보다 커지는가?

H1: 2-factor confluence Cohen's d >= 0.30 (medium effect)
   3-factor >= 0.50 (large)
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators
from _lib.weighting import get_all_weights, weighted_mean
from _lib.stats import cohen_d, interpret_d

OUT_DIR = Path(__file__).parent / "results" / "D6_confluence"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42


def to_kst(idx):
    return (idx.tz_localize("America/New_York", nonexistent="shift_forward", ambiguous="NaT")
              .tz_convert("Asia/Seoul"))


def main():
    print("[D6] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)

    # ATR z 60-day
    atr_lookback = 60 * 24 * 12
    df["atr_mean60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).mean()
    df["atr_std60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).std()
    df["atr_z"] = (df["atr14"] - df["atr_mean60d"]) / df["atr_std60d"]

    df = df.dropna(subset=["atr14", "atr_z"]).copy()

    # KST conversion
    print("[D6] Converting to KST...")
    kst_idx = to_kst(df.index)
    valid = ~kst_idx.isna()
    df = df.loc[valid].copy()
    df["kst_hour"] = kst_idx[valid].hour
    df["kst_dow"] = kst_idx[valid].dayofweek

    # Candle structure
    body = df["close"] - df["open"]
    range_ = (df["high"] - df["low"]).replace(0, np.nan)
    df["body_pct"] = body.abs() / range_
    df["body_dir"] = np.sign(body)
    df["bull_strong"] = (df["body_pct"] >= 0.7) & (df["body_dir"] > 0)
    df["bear_strong"] = (df["body_pct"] >= 0.7) & (df["body_dir"] < 0)

    # ATR z squeeze
    df["squeeze_12"] = df["atr_z"].rolling(12).max() < -0.5

    # Forward returns
    for fwd_n in [12, 24, 48]:
        df[f"fwd_{fwd_n}_signed"] = (df["close"].shift(-fwd_n) - df["close"]) / df["atr14"]
        df[f"fwd_{fwd_n}_abs"] = df[f"fwd_{fwd_n}_signed"].abs()

    # Drop NaN — use 24b as primary
    df = df.dropna(subset=["fwd_24_signed", "body_pct"])
    print(f"  bars after all filters: {len(df):,}")

    # Sample
    rng = np.random.default_rng(SEED)
    if len(df) > 80000:
        idx = rng.choice(len(df), size=80000, replace=False)
        idx.sort()
        sample = df.iloc[idx].copy()
    else:
        sample = df.copy()

    weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
    h2y = weights_all["w_h2y"]
    l2y = weights_all["last_2y"]

    # ---------- 1-factor baseline (LONG signals) ----------
    print("\n[D6] === 1-FACTOR (LONG bias signals) ===")
    print(f"{'Signal':45s} {'N':>6s} {'mu_h2y':>9s} {'mu_l2y':>9s} {'d_h2y':>8s}")

    fwd = "fwd_24_signed"
    base_signed = sample[fwd].values
    base_mean_h2y = weighted_mean(base_signed, h2y)
    base_mean_l2y = weighted_mean(base_signed, l2y)
    print(f"{'BASELINE (all bars)':45s} {len(sample):>6d} {base_mean_h2y:>+9.4f} {base_mean_l2y:>+9.4f}")

    long_signals = {
        "KST 04 (BURN_X)": (sample["kst_hour"] == 4),
        "KST 19 (pre-NY)": (sample["kst_hour"] == 19),
        "KST 14": (sample["kst_hour"] == 14),
        "Monday all-day": (sample["kst_dow"] == 0),
        "Bull strong body": sample["bull_strong"],
        "Squeeze_12": sample["squeeze_12"],
    }
    short_signals = {
        "KST 22 (BURN_R)": (sample["kst_hour"] == 22),
        "KST 21": (sample["kst_hour"] == 21),
        "KST 20": (sample["kst_hour"] == 20),
        "Tuesday all-day": (sample["kst_dow"] == 1),
        "Bear strong body": sample["bear_strong"],
    }

    results = {"baseline": {"mu_h2y": base_mean_h2y, "mu_l2y": base_mean_l2y, "n": int(len(sample))}}

    print("\n--- LONG signals ---")
    for name, mask in long_signals.items():
        sub = sample[mask]
        if len(sub) < 50: continue
        sub_idx = sample.index.get_indexer(sub.index)
        rest_idx = sample.index.get_indexer(sample[~mask].index)
        mu_h2y = weighted_mean(sub[fwd].values, h2y[sub_idx])
        mu_l2y = weighted_mean(sub[fwd].values, l2y[sub_idx])
        d = cohen_d(sub[fwd].values, sample[~mask][fwd].values, h2y[sub_idx], h2y[rest_idx])
        results[f"long_{name}"] = {"n": int(len(sub)), "mu_h2y": mu_h2y, "mu_l2y": mu_l2y, "d_h2y": d}
        print(f"{name:45s} {len(sub):>6d} {mu_h2y:>+9.4f} {mu_l2y:>+9.4f} {d:>+8.4f}")

    print("\n--- SHORT signals ---")
    for name, mask in short_signals.items():
        sub = sample[mask]
        if len(sub) < 50: continue
        sub_idx = sample.index.get_indexer(sub.index)
        rest_idx = sample.index.get_indexer(sample[~mask].index)
        mu_h2y = weighted_mean(sub[fwd].values, h2y[sub_idx])
        mu_l2y = weighted_mean(sub[fwd].values, l2y[sub_idx])
        d = cohen_d(sub[fwd].values, sample[~mask][fwd].values, h2y[sub_idx], h2y[rest_idx])
        results[f"short_{name}"] = {"n": int(len(sub)), "mu_h2y": mu_h2y, "mu_l2y": mu_l2y, "d_h2y": d}
        print(f"{name:45s} {len(sub):>6d} {mu_h2y:>+9.4f} {mu_l2y:>+9.4f} {d:>+8.4f}")

    # ---------- 2-factor confluences ----------
    print("\n[D6] === 2-FACTOR CONFLUENCES ===")
    print(f"{'Combo':55s} {'N':>5s} {'mu_h2y':>9s} {'mu_l2y':>9s} {'d_h2y':>8s}")

    confluences_long = {
        "KST 04 + Monday": (sample["kst_hour"] == 4) & (sample["kst_dow"] == 0),
        "KST 04 + bull_strong": (sample["kst_hour"] == 4) & sample["bull_strong"],
        "KST 19 + Monday": (sample["kst_hour"] == 19) & (sample["kst_dow"] == 0),
        "KST 14 + Monday": (sample["kst_hour"] == 14) & (sample["kst_dow"] == 0),
        "Squeeze_12 + Monday": sample["squeeze_12"] & (sample["kst_dow"] == 0),
        "Squeeze_12 + bull_strong": sample["squeeze_12"] & sample["bull_strong"],
        "Squeeze_12 + KST 04": sample["squeeze_12"] & (sample["kst_hour"] == 4),
        "Monday + bull_strong": (sample["kst_dow"] == 0) & sample["bull_strong"],
    }

    confluences_short = {
        "KST 22 + Tuesday": (sample["kst_hour"] == 22) & (sample["kst_dow"] == 1),
        "KST 21 + Tuesday": (sample["kst_hour"] == 21) & (sample["kst_dow"] == 1),
        "KST 22 + bear_strong": (sample["kst_hour"] == 22) & sample["bear_strong"],
        "KST 21 + bear_strong": (sample["kst_hour"] == 21) & sample["bear_strong"],
        "Tuesday + bear_strong": (sample["kst_dow"] == 1) & sample["bear_strong"],
    }

    print("\n--- LONG 2-factor ---")
    for name, mask in confluences_long.items():
        sub = sample[mask]
        if len(sub) < 30: continue
        sub_idx = sample.index.get_indexer(sub.index)
        rest_idx = sample.index.get_indexer(sample[~mask].index)
        mu_h2y = weighted_mean(sub[fwd].values, h2y[sub_idx])
        mu_l2y = weighted_mean(sub[fwd].values, l2y[sub_idx])
        d = cohen_d(sub[fwd].values, sample[~mask][fwd].values, h2y[sub_idx], h2y[rest_idx])
        results[f"long2_{name}"] = {"n": int(len(sub)), "mu_h2y": mu_h2y, "mu_l2y": mu_l2y, "d_h2y": d}
        print(f"{name:55s} {len(sub):>5d} {mu_h2y:>+9.4f} {mu_l2y:>+9.4f} {d:>+8.4f}")

    print("\n--- SHORT 2-factor ---")
    for name, mask in confluences_short.items():
        sub = sample[mask]
        if len(sub) < 30: continue
        sub_idx = sample.index.get_indexer(sub.index)
        rest_idx = sample.index.get_indexer(sample[~mask].index)
        mu_h2y = weighted_mean(sub[fwd].values, h2y[sub_idx])
        mu_l2y = weighted_mean(sub[fwd].values, l2y[sub_idx])
        d = cohen_d(sub[fwd].values, sample[~mask][fwd].values, h2y[sub_idx], h2y[rest_idx])
        results[f"short2_{name}"] = {"n": int(len(sub)), "mu_h2y": mu_h2y, "mu_l2y": mu_l2y, "d_h2y": d}
        print(f"{name:55s} {len(sub):>5d} {mu_h2y:>+9.4f} {mu_l2y:>+9.4f} {d:>+8.4f}")

    # ---------- 3-factor (top combinations) ----------
    print("\n[D6] === 3-FACTOR (top stacks) ===")
    triples_long = {
        "KST 04 + Mon + bull_strong": (sample["kst_hour"] == 4) & (sample["kst_dow"] == 0) & sample["bull_strong"],
        "KST 19 + Mon + bull_strong": (sample["kst_hour"] == 19) & (sample["kst_dow"] == 0) & sample["bull_strong"],
        "Squeeze_12 + Mon + bull_strong": sample["squeeze_12"] & (sample["kst_dow"] == 0) & sample["bull_strong"],
        "KST 04 + Mon + Squeeze_12": (sample["kst_hour"] == 4) & (sample["kst_dow"] == 0) & sample["squeeze_12"],
    }
    triples_short = {
        "KST 22 + Tue + bear_strong": (sample["kst_hour"] == 22) & (sample["kst_dow"] == 1) & sample["bear_strong"],
        "KST 21 + Tue + bear_strong": (sample["kst_hour"] == 21) & (sample["kst_dow"] == 1) & sample["bear_strong"],
    }

    for name, mask in {**triples_long, **triples_short}.items():
        sub = sample[mask]
        if len(sub) < 10:
            print(f"  {name}: SKIP (N={len(sub)} < 10)")
            continue
        sub_idx = sample.index.get_indexer(sub.index)
        rest_idx = sample.index.get_indexer(sample[~mask].index)
        mu_h2y = weighted_mean(sub[fwd].values, h2y[sub_idx])
        d = cohen_d(sub[fwd].values, sample[~mask][fwd].values, h2y[sub_idx], h2y[rest_idx])
        results[f"triple_{name}"] = {"n": int(len(sub)), "mu_h2y": mu_h2y, "d_h2y": d}
        flag = "⭐" if abs(d) >= 0.3 else ""
        print(f"  {name:50s} N={len(sub):>4d} mu_h2y={mu_h2y:>+8.4f} d={d:>+7.4f} {flag}")

    # Ranking top edges
    print("\n[D6] === TOP EDGES (sorted by |d_h2y|, N>=50) ===")
    rankable = [(k, v) for k, v in results.items() if isinstance(v, dict) and "d_h2y" in v and v["n"] >= 50]
    rankable.sort(key=lambda kv: -abs(kv[1]["d_h2y"]))
    print(f"\n{'Rank':>4s} {'Signal':<55s} {'N':>5s} {'mu_h2y':>9s} {'d_h2y':>8s}")
    for i, (k, v) in enumerate(rankable[:20], 1):
        print(f"{i:>4d} {k[:55]:<55s} {v['n']:>5d} {v['mu_h2y']:>+9.4f} {v['d_h2y']:>+8.4f}")

    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[D6] Saved → {OUT_DIR / 'results.json'}")


if __name__ == "__main__":
    main()
