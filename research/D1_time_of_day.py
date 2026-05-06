"""D1: Time-of-day forward distribution (NQ 5m, KST hour bin)

H1: KST hour 별 forward 12/24/48-bar return + |ret| 분포 다름.
    특정 hour 가 |ret| outlier (high opportunity) AND signed direction 강함.

Method:
  - Convert exchange time (FirstRateData uses ?) to KST.
    NOTE: FirstRateData NQ futures = America/New_York time (EST/EDT).
    Convert NY time → KST: KST = NY + 14h (winter EST), 13h (summer EDT).
    Use pytz to handle DST automatically.
  - Bin by KST hour 0-23
  - Forward 12/24/48 bar: |ret|/ATR + signed/ATR
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators
from _lib.weighting import get_all_weights, weighted_mean
from _lib.stats import cohen_d

OUT_DIR = Path(__file__).parent / "results" / "D1_time_of_day"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def to_kst(idx: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """FirstRateData NQ = America/New_York. KST = NY + 13h(EDT)/14h(EST).

    Use pytz tz_localize then convert to KST.
    """
    # FirstRateData typically delivers exchange time = America/New_York
    return (idx.tz_localize("America/New_York", nonexistent="shift_forward", ambiguous="NaT")
              .tz_convert("Asia/Seoul"))


def main():
    print("[D1] Loading NQ 5m + indicators...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df = df.dropna(subset=["atr14"]).copy()

    # Convert to KST
    print("[D1] Converting to KST...")
    kst_idx = to_kst(df.index)
    valid = ~kst_idx.isna()
    df = df.loc[valid].copy()
    kst_idx = kst_idx[valid]
    df["kst_hour"] = kst_idx.hour
    df["kst_dow"] = kst_idx.dayofweek    # Mon=0
    print(f"  bars (after DST handling): {len(df):,}")
    print(f"  KST hour distribution: {df['kst_hour'].value_counts().sort_index().head(24).to_dict()}")

    # Forward windows
    out = {"by_window": {}}
    for fwd_bars in [12, 24, 48]:
        df["fwd_ret"] = df["close"].shift(-fwd_bars) - df["close"]
        df["fwd_abs_ret_atr"] = df["fwd_ret"].abs() / df["atr14"]
        df["fwd_signed_ret_atr"] = df["fwd_ret"] / df["atr14"]
        d = df.dropna(subset=["fwd_abs_ret_atr"])

        # Sample 60k for speed
        rng = np.random.default_rng(42)
        if len(d) > 60000:
            idx = rng.choice(len(d), size=60000, replace=False)
            idx.sort()
            sample = d.iloc[idx]
        else:
            sample = d

        weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
        h2y = weights_all["w_h2y"]
        l2y = weights_all["last_2y"]

        per_hour = {}
        print(f"\n[D1] === fwd={fwd_bars}b ===")
        print(f"{'hr':>3s} {'N':>7s} {'|ret|h2y':>10s} {'signed_h2y':>12s} {'|ret|l2y':>10s} {'signed_l2y':>12s}")
        for h in range(24):
            sub = sample[sample["kst_hour"] == h]
            if len(sub) < 100:
                continue
            sub_idx = sample.index.get_indexer(sub.index)
            mu_abs_h2y = weighted_mean(sub["fwd_abs_ret_atr"].values, h2y[sub_idx])
            mu_signed_h2y = weighted_mean(sub["fwd_signed_ret_atr"].values, h2y[sub_idx])
            mu_abs_l2y = weighted_mean(sub["fwd_abs_ret_atr"].values, l2y[sub_idx])
            mu_signed_l2y = weighted_mean(sub["fwd_signed_ret_atr"].values, l2y[sub_idx])
            per_hour[h] = {
                "n": int(len(sub)),
                "mu_abs_h2y": mu_abs_h2y, "mu_signed_h2y": mu_signed_h2y,
                "mu_abs_l2y": mu_abs_l2y, "mu_signed_l2y": mu_signed_l2y,
            }
            print(f"{h:>3d} {len(sub):>7d} {mu_abs_h2y:>10.3f} {mu_signed_h2y:>+12.4f} {mu_abs_l2y:>10.3f} {mu_signed_l2y:>+12.4f}")

        out["by_window"][f"fwd_{fwd_bars}"] = per_hour

    # Find top opportunities
    print("\n[D1] === TOP OPPORTUNITIES (fwd=24b, w_h2y) ===")
    fwd24 = out["by_window"]["fwd_24"]

    # Top |ret| (volatility opportunities)
    sorted_abs = sorted(fwd24.items(), key=lambda x: -x[1]["mu_abs_h2y"])
    print(f"\nTop 5 hours by |ret|/ATR (high opportunity):")
    for h, r in sorted_abs[:5]:
        print(f"  KST {h:02d}: |ret|={r['mu_abs_h2y']:.3f} signed={r['mu_signed_h2y']:+.4f} N={r['n']}")
    print(f"\nBottom 3 hours by |ret|/ATR (low opportunity):")
    for h, r in sorted_abs[-3:]:
        print(f"  KST {h:02d}: |ret|={r['mu_abs_h2y']:.3f} signed={r['mu_signed_h2y']:+.4f} N={r['n']}")

    # Top signed (directional bias)
    sorted_signed = sorted(fwd24.items(), key=lambda x: -x[1]["mu_signed_h2y"])
    print(f"\nTop 3 hours by signed return (LONG bias):")
    for h, r in sorted_signed[:3]:
        print(f"  KST {h:02d}: signed={r['mu_signed_h2y']:+.4f} |ret|={r['mu_abs_h2y']:.3f} N={r['n']}")
    print(f"\nBottom 3 hours by signed return (SHORT bias):")
    for h, r in sorted_signed[-3:]:
        print(f"  KST {h:02d}: signed={r['mu_signed_h2y']:+.4f} |ret|={r['mu_abs_h2y']:.3f} N={r['n']}")

    out["top_opportunities"] = {
        "fwd_24b_by_abs_ret": [{"hour": h, **r} for h, r in sorted_abs],
        "fwd_24b_by_signed": [{"hour": h, **r} for h, r in sorted_signed],
    }

    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[D1] Saved → {OUT_DIR / 'results.json'}")


if __name__ == "__main__":
    main()
