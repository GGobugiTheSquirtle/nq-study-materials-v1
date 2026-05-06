"""D2-D5 batch discovery research.

D2: Mean reversion / momentum windows (recent N-bar return → forward)
D3: Volatility expansion transition (low z period → high z transition)
D4: Candle structure (body/range, wick) → forward direction
D5: Day of week effect
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators
from _lib.weighting import get_all_weights, weighted_mean

OUT_DIR = Path(__file__).parent / "results"
SEED = 42


def to_kst(idx):
    return (idx.tz_localize("America/New_York", nonexistent="shift_forward", ambiguous="NaT")
              .tz_convert("Asia/Seoul"))


def D2_mean_reversion(df: pd.DataFrame):
    """Recent N-bar return → forward N-bar return. Mean revert vs momentum?"""
    print("\n[D2] Mean reversion vs momentum")
    out_dir = OUT_DIR / "D2_mean_reversion"
    out_dir.mkdir(parents=True, exist_ok=True)

    out = {}
    for past_n in [3, 6, 12, 24]:
        for fwd_n in [3, 12, 24]:
            df["past_ret_atr"] = (df["close"] - df["close"].shift(past_n)) / df["atr14"]
            df["fwd_ret_atr"] = (df["close"].shift(-fwd_n) - df["close"]) / df["atr14"]
            d = df.dropna(subset=["past_ret_atr", "fwd_ret_atr"])

            rng = np.random.default_rng(SEED)
            if len(d) > 30000:
                idx = rng.choice(len(d), size=30000, replace=False)
                idx.sort()
                sample = d.iloc[idx]
            else:
                sample = d

            weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
            h2y = weights_all["w_h2y"]

            # Pearson correlation (weighted)
            x = sample["past_ret_atr"].values
            y = sample["fwd_ret_atr"].values
            mu_x = weighted_mean(x, h2y)
            mu_y = weighted_mean(y, h2y)
            num = np.sum(h2y * (x - mu_x) * (y - mu_y))
            den_x = np.sqrt(np.sum(h2y * (x - mu_x) ** 2))
            den_y = np.sqrt(np.sum(h2y * (y - mu_y) ** 2))
            corr = num / (den_x * den_y) if (den_x > 0 and den_y > 0) else 0.0

            # By past_ret bin: extreme moves predict reversal?
            sample = sample.copy()
            def bin_past(r):
                if r < -1.5: return "extreme down"
                if r < -0.5: return "moderate down"
                if r < +0.5: return "flat"
                if r < +1.5: return "moderate up"
                return "extreme up"
            sample["bin"] = sample["past_ret_atr"].apply(bin_past)

            bin_results = {}
            for b in ["extreme down", "moderate down", "flat", "moderate up", "extreme up"]:
                sub = sample[sample["bin"] == b]
                if len(sub) < 100: continue
                sub_idx = sample.index.get_indexer(sub.index)
                mu_fwd = weighted_mean(sub["fwd_ret_atr"].values, h2y[sub_idx])
                bin_results[b] = {"n": int(len(sub)), "mu_fwd_h2y": mu_fwd}

            out[f"past_{past_n}_fwd_{fwd_n}"] = {
                "corr_h2y": corr,
                "bin_results": bin_results,
            }
            print(f"  past={past_n:>2d}b fwd={fwd_n:>2d}b: corr={corr:+.4f}")
            for b, r in bin_results.items():
                print(f"    {b:15s} N={r['n']:>5d} mu_fwd_h2y={r['mu_fwd_h2y']:+.4f}")

    with open(out_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    return out


def D3_vol_expansion(df: pd.DataFrame):
    """Low z period → forward bigger range? Squeeze breakout test."""
    print("\n[D3] Volatility expansion (low z → next range)")
    out_dir = OUT_DIR / "D3_vol_expansion"
    out_dir.mkdir(parents=True, exist_ok=True)

    atr_lookback = 60 * 24 * 12
    df["atr_mean60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).mean()
    df["atr_std60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).std()
    df["atr_z"] = (df["atr14"] - df["atr_mean60d"]) / df["atr_std60d"]

    # Detect "squeeze" = N consecutive bars of z < threshold
    df["squeeze_3"] = df["atr_z"].rolling(3).max() < -0.5
    df["squeeze_6"] = df["atr_z"].rolling(6).max() < -0.5
    df["squeeze_12"] = df["atr_z"].rolling(12).max() < -0.5

    out = {}
    for fwd_n in [12, 24, 48]:
        df["fwd_range"] = df["high"].rolling(fwd_n).max().shift(-fwd_n) - df["low"].rolling(fwd_n).min().shift(-fwd_n)
        df["fwd_range_atr"] = df["fwd_range"] / df["atr14"]
        df["fwd_signed"] = (df["close"].shift(-fwd_n) - df["close"]) / df["atr14"]
        d = df.dropna(subset=["fwd_range_atr", "atr_z"])

        rng = np.random.default_rng(SEED)
        if len(d) > 60000:
            idx = rng.choice(len(d), size=60000, replace=False)
            idx.sort()
            sample = d.iloc[idx]
        else:
            sample = d

        weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
        h2y = weights_all["w_h2y"]

        # Squeeze vs no-squeeze comparison
        results = {}
        for sq_col in ["squeeze_3", "squeeze_6", "squeeze_12"]:
            in_sq = sample[sample[sq_col]]
            no_sq = sample[~sample[sq_col]]
            if len(in_sq) < 100 or len(no_sq) < 100:
                continue
            sq_idx = sample.index.get_indexer(in_sq.index)
            no_idx = sample.index.get_indexer(no_sq.index)
            mu_sq_range = weighted_mean(in_sq["fwd_range_atr"].values, h2y[sq_idx])
            mu_no_range = weighted_mean(no_sq["fwd_range_atr"].values, h2y[no_idx])
            mu_sq_signed = weighted_mean(in_sq["fwd_signed"].values, h2y[sq_idx])
            mu_no_signed = weighted_mean(no_sq["fwd_signed"].values, h2y[no_idx])
            results[sq_col] = {
                "n_sq": int(len(in_sq)), "n_no": int(len(no_sq)),
                "mu_sq_range_h2y": mu_sq_range, "mu_no_range_h2y": mu_no_range, "delta_range": mu_sq_range - mu_no_range,
                "mu_sq_signed_h2y": mu_sq_signed, "mu_no_signed_h2y": mu_no_signed,
            }
            print(f"  fwd={fwd_n}b {sq_col}: range_sq={mu_sq_range:.3f} range_no={mu_no_range:.3f} Δ={mu_sq_range-mu_no_range:+.3f} | signed_sq={mu_sq_signed:+.4f}")

        out[f"fwd_{fwd_n}"] = results

    with open(out_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    return out


def D4_candle_structure(df: pd.DataFrame):
    """Candle body / wick ratio → next bar direction."""
    print("\n[D4] Candle structure → forward direction")
    out_dir = OUT_DIR / "D4_candle_structure"
    out_dir.mkdir(parents=True, exist_ok=True)

    body = df["close"] - df["open"]
    range_ = df["high"] - df["low"]
    upper_wick = df["high"] - df[["close", "open"]].max(axis=1)
    lower_wick = df[["close", "open"]].min(axis=1) - df["low"]
    df["body_pct"] = body.abs() / range_.replace(0, np.nan)
    df["upper_wick_pct"] = upper_wick / range_.replace(0, np.nan)
    df["lower_wick_pct"] = lower_wick / range_.replace(0, np.nan)
    df["body_dir"] = np.sign(body)

    out = {}
    for fwd_n in [3, 12, 24]:
        df["fwd_signed"] = (df["close"].shift(-fwd_n) - df["close"]) / df["atr14"]
        d = df.dropna(subset=["body_pct", "fwd_signed"])

        rng = np.random.default_rng(SEED)
        if len(d) > 30000:
            idx = rng.choice(len(d), size=30000, replace=False)
            idx.sort()
            sample = d.iloc[idx]
        else:
            sample = d

        weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
        h2y = weights_all["w_h2y"]

        # Bullish strong body (body_pct >= 0.7, body_dir > 0)
        sample = sample.copy()
        cond_bull_strong = (sample["body_pct"] >= 0.7) & (sample["body_dir"] > 0)
        cond_bear_strong = (sample["body_pct"] >= 0.7) & (sample["body_dir"] < 0)
        cond_bull_pin = (sample["lower_wick_pct"] >= 0.5) & (sample["body_pct"] < 0.4)   # hammer-like
        cond_bear_pin = (sample["upper_wick_pct"] >= 0.5) & (sample["body_pct"] < 0.4)   # shooting star
        cond_doji = sample["body_pct"] < 0.15

        results = {}
        for cname, cmask in [
            ("bull_strong_body", cond_bull_strong),
            ("bear_strong_body", cond_bear_strong),
            ("bull_pin_hammer", cond_bull_pin),
            ("bear_pin_shoot_star", cond_bear_pin),
            ("doji", cond_doji),
        ]:
            sub = sample[cmask]
            if len(sub) < 100: continue
            sub_idx = sample.index.get_indexer(sub.index)
            mu_signed = weighted_mean(sub["fwd_signed"].values, h2y[sub_idx])
            mu_signed_l2y = weighted_mean(sub["fwd_signed"].values, weights_all["last_2y"][sub_idx])
            results[cname] = {"n": int(len(sub)), "mu_signed_h2y": mu_signed, "mu_signed_l2y": mu_signed_l2y}

        out[f"fwd_{fwd_n}"] = results
        print(f"  fwd={fwd_n}b:")
        for c, r in results.items():
            print(f"    {c:25s} N={r['n']:>5d} signed_h2y={r['mu_signed_h2y']:+.4f} signed_l2y={r['mu_signed_l2y']:+.4f}")

    with open(out_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    return out


def D5_day_of_week(df: pd.DataFrame):
    """Day of week effect."""
    print("\n[D5] Day of week effect")
    out_dir = OUT_DIR / "D5_dow"
    out_dir.mkdir(parents=True, exist_ok=True)

    kst_idx = to_kst(df.index)
    valid = ~kst_idx.isna()
    df = df.loc[valid].copy()
    df["kst_dow"] = kst_idx[valid].dayofweek    # Mon=0, Sun=6

    out = {}
    for fwd_n in [12, 24, 48]:
        df["fwd_signed"] = (df["close"].shift(-fwd_n) - df["close"]) / df["atr14"]
        df["fwd_abs"] = df["fwd_signed"].abs()
        d = df.dropna(subset=["fwd_signed"])

        rng = np.random.default_rng(SEED)
        if len(d) > 50000:
            idx = rng.choice(len(d), size=50000, replace=False)
            idx.sort()
            sample = d.iloc[idx]
        else:
            sample = d

        weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
        h2y = weights_all["w_h2y"]

        dow_names = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
        results = {}
        print(f"  fwd={fwd_n}b:")
        for d_num in range(7):
            sub = sample[sample["kst_dow"] == d_num]
            if len(sub) < 100: continue
            sub_idx = sample.index.get_indexer(sub.index)
            mu_signed = weighted_mean(sub["fwd_signed"].values, h2y[sub_idx])
            mu_abs = weighted_mean(sub["fwd_abs"].values, h2y[sub_idx])
            results[dow_names[d_num]] = {"n": int(len(sub)), "mu_signed_h2y": mu_signed, "mu_abs_h2y": mu_abs}
            print(f"    {dow_names[d_num]:5s} N={len(sub):>5d} signed={mu_signed:+.4f} |ret|={mu_abs:.3f}")

        out[f"fwd_{fwd_n}"] = results

    with open(out_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    return out


def main():
    print("[D2-D5] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df = df.dropna(subset=["atr14"])

    D2_mean_reversion(df.copy())
    D3_vol_expansion(df.copy())
    D4_candle_structure(df.copy())
    D5_day_of_week(df.copy())

    print("\n[D2-D5] All done.")


if __name__ == "__main__":
    main()
