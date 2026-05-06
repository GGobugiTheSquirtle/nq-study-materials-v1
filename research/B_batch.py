"""B1+B2+B4 batch.

B1: SR zone (touch≥3) vs line (single price) — MFE 0.5×ATR hit rate
B2: BB(20, 2σ) NQ 5m 95% rule check + walking-the-band
B4: Multi-TF alignment (5m + 15m + 1h all-up) effect
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators, ema
from _lib.weighting import get_all_weights, weighted_mean
from _lib.stats import cohen_d, hit_rate
from _lib.path_sim import forward_mfe_mae

OUT_DIR = Path(__file__).parent / "results"
SEED = 42


def B1_sr_zone_vs_line(df: pd.DataFrame):
    """SR zone (touch≥3 within ±0.25×ATR) vs line (single price).

    Test: 가격이 SR zone 진입할 때 vs 단일 swing point 정확히 통과할 때
    forward MFE 0.5×ATR (반대방향) 도달률 비교.
    """
    print("\n[B1] SR zone vs single line")
    out_dir = OUT_DIR / "B1_sr_zone_vs_line"
    out_dir.mkdir(parents=True, exist_ok=True)

    high = df["high"].values
    low = df["low"].values
    close = df["close"].values
    atr = df["atr14"].values
    n = len(df)

    # Step 1: Detect swing pivots (fractal, ±5 bars)
    LB = 5
    is_swing_high = np.zeros(n, dtype=bool)
    is_swing_low = np.zeros(n, dtype=bool)
    for i in range(LB, n - LB):
        if high[i] == high[i - LB:i + LB + 1].max():
            is_swing_high[i] = True
        if low[i] == low[i - LB:i + LB + 1].min():
            is_swing_low[i] = True

    swing_high_indices = np.where(is_swing_high)[0]
    swing_low_indices = np.where(is_swing_low)[0]
    print(f"  swing highs: {len(swing_high_indices):,}, swing lows: {len(swing_low_indices):,}")

    # Step 2: Cluster swings into zones (±0.25×ATR within last 500 bars window)
    # For each bar i, check: did price recently enter a "valid zone" (touch≥3)?
    # Test events: when price (low) touches a resistance zone (validated swing high cluster)

    # Simplified: at bar i, look back 500 bars at swing highs.
    # Cluster swing highs by ±0.25×ATR. Find max-touch cluster.
    # If current high is within that cluster, this is a "zone touch event".
    # Track for both resistance (swing highs) and support (swing lows).

    zone_touch_events = []   # (idx, event_type, n_touches_in_zone, atr)
    line_touch_events = []   # (idx, event_type, single_swing_idx, atr)

    LOOKBACK_BARS = 500
    print(f"  scanning {n:,} bars for SR events (sampled)...")

    # Sample to keep manageable
    rng = np.random.default_rng(SEED)
    sample_idx = rng.choice(np.arange(LOOKBACK_BARS, n - 50), size=min(50000, n - LOOKBACK_BARS - 50), replace=False)
    sample_idx.sort()

    for i in sample_idx:
        atr_i = atr[i]
        if atr_i <= 0 or np.isnan(atr_i):
            continue
        zone_w = 0.25 * atr_i
        # Recent swing highs in window
        sh_in_win = swing_high_indices[(swing_high_indices >= i - LOOKBACK_BARS) & (swing_high_indices < i)]
        sl_in_win = swing_low_indices[(swing_low_indices >= i - LOOKBACK_BARS) & (swing_low_indices < i)]

        # Resistance: cluster swing high prices ±zone_w around current high
        if len(sh_in_win) > 0:
            sh_prices = high[sh_in_win]
            # Find cluster centered on current high
            mask = np.abs(sh_prices - high[i]) <= zone_w
            n_touches = int(mask.sum())
            if n_touches >= 3:
                zone_touch_events.append((i, "resist_zone", n_touches, atr_i))
            elif n_touches >= 1:
                # Closest single price
                line_touch_events.append((i, "resist_line", n_touches, atr_i))

        if len(sl_in_win) > 0:
            sl_prices = low[sl_in_win]
            mask = np.abs(sl_prices - low[i]) <= zone_w
            n_touches = int(mask.sum())
            if n_touches >= 3:
                zone_touch_events.append((i, "support_zone", n_touches, atr_i))
            elif n_touches >= 1:
                line_touch_events.append((i, "support_line", n_touches, atr_i))

    print(f"  zone events (touch≥3): {len(zone_touch_events):,}")
    print(f"  line events (touch=1-2): {len(line_touch_events):,}")

    # Step 3: For each event, simulate forward MFE in expected direction
    # resist → expect SHORT (price down). support → expect LONG.
    def evaluate_events(events, fwd_bars=12):
        rows = []
        for idx, etype, n_t, atr_i in events:
            if idx + fwd_bars >= n:
                continue
            fwd_high = high[idx + 1: idx + 1 + fwd_bars].max()
            fwd_low = low[idx + 1: idx + 1 + fwd_bars].min()
            if "resist" in etype:
                # SHORT: MFE down = current_close - fwd_low
                mfe = close[idx] - fwd_low
                direction = "short"
            else:
                mfe = fwd_high - close[idx]
                direction = "long"
            rows.append({
                "idx": idx, "etype": etype, "n_touches": n_t,
                "atr": atr_i, "mfe_atr": mfe / atr_i,
                "datetime": df.index[idx],
            })
        return pd.DataFrame(rows)

    zone_df = evaluate_events(zone_touch_events)
    line_df = evaluate_events(line_touch_events)
    print(f"  zone valid events: {len(zone_df):,}")
    print(f"  line valid events: {len(line_df):,}")

    # Compare hit rate (MFE >= 0.5×ATR in expected direction)
    out = {}
    for thresh in [0.5, 1.0]:
        zone_idx = pd.DatetimeIndex(zone_df["datetime"])
        line_idx = pd.DatetimeIndex(line_df["datetime"])
        zw = get_all_weights(zone_idx)["w_h2y"]
        lw = get_all_weights(line_idx)["w_h2y"]
        zone_hr = hit_rate(zone_df["mfe_atr"].values, zw, thresh, ">=")
        line_hr = hit_rate(line_df["mfe_atr"].values, lw, thresh, ">=")
        delta_pp = (zone_hr - line_hr) * 100
        out[f"thresh_{thresh}"] = {
            "zone_hr_h2y": zone_hr, "line_hr_h2y": line_hr,
            "delta_pp": delta_pp,
            "n_zone": int(len(zone_df)), "n_line": int(len(line_df)),
        }
        print(f"  MFE >= {thresh}×ATR: zone HR={zone_hr*100:.2f}% line HR={line_hr*100:.2f}% Δ={delta_pp:+.2f}pp")

    # By touch count (within zones)
    print("\n  Hit rate by zone touch count (h2y):")
    for tc in [3, 4, 5, 6]:
        sub = zone_df[zone_df["n_touches"] >= tc]
        if len(sub) < 50: continue
        zw = get_all_weights(pd.DatetimeIndex(sub["datetime"]))["w_h2y"]
        hr = hit_rate(sub["mfe_atr"].values, zw, 0.5, ">=")
        print(f"    touch>={tc}: HR={hr*100:.2f}% N={len(sub)}")

    with open(out_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    return out


def B2_bb_95_rule(df: pd.DataFrame):
    """BB(20, 2σ) NQ 5m: 95% 가격 rule + walking-the-band."""
    print("\n[B2] BB 95% rule + walking-the-band check")
    out_dir = OUT_DIR / "B2_bb_check"
    out_dir.mkdir(parents=True, exist_ok=True)

    sma20 = df["close"].rolling(20).mean()
    std20 = df["close"].rolling(20).std()
    upper = sma20 + 2 * std20
    lower = sma20 - 2 * std20
    df["bb_upper"] = upper
    df["bb_lower"] = lower
    df["bb_mid"] = sma20
    df["bb_width"] = upper - lower
    df = df.dropna(subset=["bb_upper", "atr14"])

    # 95% rule: % bars where close within [lower, upper]
    inside = ((df["close"] >= df["bb_lower"]) & (df["close"] <= df["bb_upper"]))
    above = df["close"] > df["bb_upper"]
    below = df["close"] < df["bb_lower"]

    # Sample
    rng = np.random.default_rng(SEED)
    if len(df) > 100000:
        idx = rng.choice(len(df), size=100000, replace=False)
        idx.sort()
        sample = df.iloc[idx]
    else:
        sample = df

    weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
    h2y = weights_all["w_h2y"]

    inside_pct_eq = float(inside.loc[sample.index].mean()) * 100
    inside_pct_h2y = float(weighted_mean(inside.loc[sample.index].values.astype(float), h2y)) * 100
    above_pct = float(weighted_mean(above.loc[sample.index].values.astype(float), h2y)) * 100
    below_pct = float(weighted_mean(below.loc[sample.index].values.astype(float), h2y)) * 100

    print(f"  Inside BB (eq weight): {inside_pct_eq:.2f}%")
    print(f"  Inside BB (h2y):       {inside_pct_h2y:.2f}%")
    print(f"  Above upper:           {above_pct:.2f}%")
    print(f"  Below lower:           {below_pct:.2f}%")
    print(f"  → Theoretical 95% rule {'CONFIRMED' if 93 <= inside_pct_h2y <= 97 else 'DEVIATES'}")

    # Walking-the-band: after upper touch, what's forward signed return?
    upper_touch = (df["close"] >= df["bb_upper"])
    lower_touch = (df["close"] <= df["bb_lower"])
    df["fwd_12_signed"] = (df["close"].shift(-12) - df["close"]) / df["atr14"]

    upper_sub = df[upper_touch].dropna(subset=["fwd_12_signed"])
    lower_sub = df[lower_touch].dropna(subset=["fwd_12_signed"])

    if len(upper_sub) > 100:
        sample_upper = upper_sub.sample(min(20000, len(upper_sub)), random_state=42)
        h2y_u = get_all_weights(pd.DatetimeIndex(sample_upper.index))["w_h2y"]
        mu_after_upper = weighted_mean(sample_upper["fwd_12_signed"].values, h2y_u)
        print(f"  After upper touch: fwd 12b signed = {mu_after_upper:+.4f} ATR (N={len(sample_upper):,})")
    else:
        mu_after_upper = None

    if len(lower_sub) > 100:
        sample_lower = lower_sub.sample(min(20000, len(lower_sub)), random_state=42)
        h2y_l = get_all_weights(pd.DatetimeIndex(sample_lower.index))["w_h2y"]
        mu_after_lower = weighted_mean(sample_lower["fwd_12_signed"].values, h2y_l)
        print(f"  After lower touch: fwd 12b signed = {mu_after_lower:+.4f} ATR (N={len(sample_lower):,})")
    else:
        mu_after_lower = None

    out = {
        "inside_pct_eq": inside_pct_eq,
        "inside_pct_h2y": inside_pct_h2y,
        "above_pct_h2y": above_pct,
        "below_pct_h2y": below_pct,
        "rule_95_status": "CONFIRMED" if 93 <= inside_pct_h2y <= 97 else "DEVIATES",
        "walking_band_after_upper": mu_after_upper,
        "walking_band_after_lower": mu_after_lower,
    }

    with open(out_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    return out


def B4_multi_tf_alignment(df_5m: pd.DataFrame):
    """Multi-TF alignment: 5m + 15m + 1h all-up vs mixed."""
    print("\n[B4] Multi-TF alignment (5m + 15m + 1h)")
    out_dir = OUT_DIR / "B4_multi_tf"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Add 15m + 1h EMA20 (resampled to 5m index)
    # 15m equivalent in 5m bars = 3
    # 1h equivalent in 5m bars = 12
    df_5m["ema20_15m"] = df_5m["close"].ewm(span=20*3, adjust=False).mean()    # approximation
    df_5m["ema20_1h"] = df_5m["close"].ewm(span=20*12, adjust=False).mean()

    df_5m["align_5m"] = df_5m["close"] > df_5m["ema20"]
    df_5m["align_15m"] = df_5m["close"] > df_5m["ema20_15m"]
    df_5m["align_1h"] = df_5m["close"] > df_5m["ema20_1h"]
    df_5m["all_up"] = df_5m["align_5m"] & df_5m["align_15m"] & df_5m["align_1h"]
    df_5m["all_down"] = (~df_5m["align_5m"]) & (~df_5m["align_15m"]) & (~df_5m["align_1h"])

    df_5m["fwd_12_signed"] = (df_5m["close"].shift(-12) - df_5m["close"]) / df_5m["atr14"]
    df_5m["fwd_24_signed"] = (df_5m["close"].shift(-24) - df_5m["close"]) / df_5m["atr14"]

    d = df_5m.dropna(subset=["all_up", "fwd_12_signed", "fwd_24_signed"])
    rng = np.random.default_rng(SEED)
    if len(d) > 100000:
        idx = rng.choice(len(d), size=100000, replace=False)
        idx.sort()
        sample = d.iloc[idx]
    else:
        sample = d

    weights_all = get_all_weights(pd.DatetimeIndex(sample.index))
    h2y = weights_all["w_h2y"]
    l2y = weights_all["last_2y"]

    out = {}
    for fwd in [12, 24]:
        col = f"fwd_{fwd}_signed"
        all_up_mask = sample["all_up"]
        all_down_mask = sample["all_down"]
        mixed_mask = (~all_up_mask) & (~all_down_mask)

        sub_up = sample[all_up_mask]
        sub_dn = sample[all_down_mask]
        sub_mx = sample[mixed_mask]
        sub_up_idx = sample.index.get_indexer(sub_up.index)
        sub_dn_idx = sample.index.get_indexer(sub_dn.index)
        sub_mx_idx = sample.index.get_indexer(sub_mx.index)

        mu_up = weighted_mean(sub_up[col].values, h2y[sub_up_idx])
        mu_dn = weighted_mean(sub_dn[col].values, h2y[sub_dn_idx])
        mu_mx = weighted_mean(sub_mx[col].values, h2y[sub_mx_idx])
        d_updn = cohen_d(sub_up[col].values, sub_dn[col].values, h2y[sub_up_idx], h2y[sub_dn_idx])

        mu_up_l2y = weighted_mean(sub_up[col].values, l2y[sub_up_idx])
        mu_dn_l2y = weighted_mean(sub_dn[col].values, l2y[sub_dn_idx])

        out[f"fwd_{fwd}"] = {
            "n_all_up": int(len(sub_up)), "n_all_down": int(len(sub_dn)), "n_mixed": int(len(sub_mx)),
            "mu_up_h2y": mu_up, "mu_down_h2y": mu_dn, "mu_mixed_h2y": mu_mx,
            "mu_up_l2y": mu_up_l2y, "mu_down_l2y": mu_dn_l2y,
            "cohen_d_h2y": d_updn,
        }
        print(f"  fwd={fwd}b: all-up mu_h2y={mu_up:+.4f} l2y={mu_up_l2y:+.4f} N={len(sub_up):,}")
        print(f"             all-down mu_h2y={mu_dn:+.4f} l2y={mu_dn_l2y:+.4f} N={len(sub_dn):,}")
        print(f"             mixed mu_h2y={mu_mx:+.4f} N={len(sub_mx):,}")
        print(f"             d(up vs down) = {d_updn:+.4f}")

    with open(out_dir / "results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    return out


def main():
    print("[B] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df = df.dropna(subset=["atr14"])

    B1_sr_zone_vs_line(df.copy())
    B2_bb_95_rule(df.copy())
    B4_multi_tf_alignment(df.copy())

    print("\n[B] All done.")


if __name__ == "__main__":
    main()
