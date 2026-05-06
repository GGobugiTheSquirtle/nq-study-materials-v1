"""Phase G2: Round Figures — Deep dive (corrections + extensions)

Improvements vs G:
  1. Cross detection: gap-safe (uses prev_CLOSE not prev_high)
  2. Swing high/low: 진짜 pivot fractal (5-5 confirmed, 10-10 strict)
     - Rolling max (G's method) is NOT true swing — no left context
     - Pivot fractal: high[i-N] > high[i-2N..i-N-1] AND > high[i-N+1..i]
  3. Forward return: entry @ next bar open (실전 entry 시점)
  4. Cost-adjusted: 0.022 ATR/RT 차감
  5. KST hour × round confluence (time-of-day effect)
  6. Failed breakout pattern (round break + reverse within 3 bars)

Key Hypotheses (refined):
  H1a: R1000 down + true swing low (pivot 5-5, broken) → LONG bounce P3 PF > 1.05
  H1b: R1000 up + true swing high (pivot 5-5, broken) → SHORT continuation OR bounce
  H1c: KST 14/19 + R500/R1000 down + SL → super-confluence
  H1d: 사용자 직관 "전고점 + 라운드 SHORT": pivot-based 검증 시 last_2y consistent?

Method: NQ 5m 10y, full sweep + cost-adjusted trade sim.
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

OUT_DIR = Path(__file__).parent / "results" / "G2_round_deep"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COST_ATR = 0.022
SEED = 42


def to_kst(idx):
    return (idx.tz_localize("America/New_York", nonexistent="shift_forward", ambiguous="NaT")
              .tz_convert("Asia/Seoul"))


def detect_crosses_v2(df: pd.DataFrame, round_step: int) -> pd.DataFrame:
    """Gap-safe cross detection using prev_CLOSE as reference.

    Up-cross: prev_close < round_value AND high >= round_value (round 가 [prev_close, high] 안)
    Down-cross: prev_close > round_value AND low <= round_value
    """
    close = df["close"].values
    high = df["high"].values
    low = df["low"].values
    n = len(df)
    events = []
    for i in range(1, n):
        prev_c = close[i - 1]

        # Up-cross
        r_above_prev = (np.floor(prev_c / round_step) + 1) * round_step
        if r_above_prev <= high[i]:
            events.append({
                "idx": i, "direction": "up",
                "round_value": float(r_above_prev),
                "round_step": round_step,
            })

        # Down-cross
        r_below_prev = (np.ceil(prev_c / round_step) - 1) * round_step
        if r_below_prev >= low[i]:
            events.append({
                "idx": i, "direction": "down",
                "round_value": float(r_below_prev),
                "round_step": round_step,
            })
    return pd.DataFrame(events)


def detect_pivots(df: pd.DataFrame, n_left: int, n_right: int):
    """Detect confirmed pivot highs/lows.

    Pivot high at bar i = high[i] is max in [i-n_left, i+n_right]
    Pivot is confirmed at bar (i + n_right) — N bar lag.
    """
    high = df["high"].values
    low = df["low"].values
    n = len(df)

    # Track confirmed pivot highs / lows
    # At bar t, the most recent confirmed pivot high is from bar i = t - n_right
    # (if high[i] was max in [i-n_left, i+n_right])
    confirmed_pivot_highs = []   # list of (bar_idx, price)
    confirmed_pivot_lows = []

    for t in range(n_left + n_right, n):
        i = t - n_right
        if i < n_left:
            continue
        window_high = high[i - n_left: i + n_right + 1]
        if high[i] == window_high.max():
            confirmed_pivot_highs.append((i, high[i], t))    # (pivot_bar, price, confirmed_bar)

        window_low = low[i - n_left: i + n_right + 1]
        if low[i] == window_low.min():
            confirmed_pivot_lows.append((i, low[i], t))

    return confirmed_pivot_highs, confirmed_pivot_lows


def get_recent_pivot_price(pivots, current_bar, max_age_bars=200):
    """Get most recent confirmed pivot (high or low) price before current_bar.
    max_age = limit search to recent pivots (avoid ancient).
    """
    # pivots is list of (pivot_bar, price, confirmed_bar)
    valid = [(b, p, c) for b, p, c in pivots if c <= current_bar and (current_bar - b) <= max_age_bars]
    if not valid:
        return None
    valid.sort(key=lambda x: -x[0])    # most recent pivot first
    return valid[0][1]


def measure_forward_with_entry(df: pd.DataFrame, events: pd.DataFrame, fwd_bars: int = 24):
    """Forward return measured with ENTRY at next bar open."""
    open_ = df["open"].values
    high = df["high"].values
    low = df["low"].values
    close = df["close"].values
    atr = df["atr14"].values
    n = len(df)

    rows = []
    for _, ev in events.iterrows():
        idx = int(ev["idx"])
        if idx + 1 + fwd_bars >= n:
            continue
        atr_i = atr[idx]
        if atr_i <= 0 or np.isnan(atr_i):
            continue
        entry = open_[idx + 1]   # entry @ next bar open
        future_high = high[idx + 1: idx + 1 + fwd_bars + 1].max()
        future_low = low[idx + 1: idx + 1 + fwd_bars + 1].min()
        future_close = close[idx + fwd_bars]

        signed_pre = (future_close - entry) / atr_i
        signed_post_cost = signed_pre - COST_ATR    # rough single-side cost (since we measure direction)

        if ev["direction"] == "up":
            rev_mfe = (entry - future_low) / atr_i
            cont_mfe = (future_high - entry) / atr_i
        else:
            rev_mfe = (future_high - entry) / atr_i
            cont_mfe = (entry - future_low) / atr_i

        rows.append({
            "idx": idx,
            "datetime": df.index[idx],
            "direction": ev["direction"],
            "round_step": ev["round_step"],
            "round_value": ev["round_value"],
            "atr": atr_i,
            "entry": entry,
            "signed_pre_cost": signed_pre,
            "signed_atr": signed_post_cost,
            "rev_mfe_atr": rev_mfe,
            "cont_mfe_atr": cont_mfe,
        })
    return pd.DataFrame(rows)


def stats_summary(df: pd.DataFrame):
    if len(df) == 0:
        return None
    times = pd.DatetimeIndex(df["datetime"])
    weights = get_all_weights(times)
    out = {"n": int(len(df))}
    for sch_name, w in weights.items():
        out[sch_name] = {
            "mu_signed_post_cost": weighted_mean(df["signed_atr"].values, w),
            "mu_signed_pre_cost":  weighted_mean(df["signed_pre_cost"].values, w),
            "mu_rev_mfe":          weighted_mean(df["rev_mfe_atr"].values, w),
            "mu_cont_mfe":         weighted_mean(df["cont_mfe_atr"].values, w),
        }
    # Period split
    df_p = df.copy()
    df_p["dt"] = pd.to_datetime(df_p["datetime"])
    df_p["period"] = "P3_2023+"
    df_p.loc[df_p["dt"].dt.year <= 2019, "period"] = "P1_2016_2019"
    df_p.loc[(df_p["dt"].dt.year >= 2020) & (df_p["dt"].dt.year <= 2022), "period"] = "P2_2020_2022"
    out["by_period"] = {}
    for p in ["P1_2016_2019", "P2_2020_2022", "P3_2023+"]:
        sub = df_p[df_p["period"] == p]
        if len(sub) > 0:
            out["by_period"][p] = {
                "n": int(len(sub)),
                "mu_signed_post_cost": float(sub["signed_atr"].mean()),
                "mu_signed_pre_cost":  float(sub["signed_pre_cost"].mean()),
            }
    return out


def trade_sim_simple(df: pd.DataFrame, events: pd.DataFrame, direction: str,
                     sl_atr=1.5, tp_atr=2.0, max_hold=24):
    """Simple SL/TP trade sim (path-sim SL-first), cost-adjusted."""
    open_ = df["open"].values
    high = df["high"].values
    low = df["low"].values
    close = df["close"].values
    atr = df["atr14"].values
    n = len(df)
    sign = +1 if direction == "long" else -1
    rows = []
    for _, ev in events.iterrows():
        idx = int(ev["idx"])
        if idx + 1 + max_hold >= n:
            continue
        atr_i = atr[idx]
        if atr_i <= 0 or np.isnan(atr_i):
            continue
        entry = open_[idx + 1]
        sl = entry - sign * sl_atr * atr_i
        tp = entry + sign * tp_atr * atr_i
        hit = "time"
        exit_p = open_[idx + 1 + max_hold]
        for k in range(1, max_hold + 1):
            j = idx + 1 + k
            if j >= n: break
            h, l = high[j], low[j]
            if direction == "long":
                if l <= sl: exit_p = sl; hit = "sl"; break
                if h >= tp: exit_p = tp; hit = "tp"; break
            else:
                if h >= sl: exit_p = sl; hit = "sl"; break
                if l <= tp: exit_p = tp; hit = "tp"; break
        pnl_pre = sign * (exit_p - entry) / atr_i
        pnl = pnl_pre - COST_ATR
        rows.append({
            "idx": idx, "datetime": ev["datetime"],
            "pnl_atr": pnl, "hit": hit,
        })
    if not rows: return None
    tdf = pd.DataFrame(rows)
    wins = tdf[tdf["pnl_atr"] > 0]
    losses = tdf[tdf["pnl_atr"] <= 0]
    n_t = len(tdf)
    pf = wins["pnl_atr"].sum() / -losses["pnl_atr"].sum() if losses["pnl_atr"].sum() < 0 else float("inf")
    wr = len(wins) / n_t
    expectancy = tdf["pnl_atr"].mean()

    # P3 split
    tdf["dt"] = pd.to_datetime(tdf["datetime"])
    p3 = tdf[tdf["dt"].dt.year >= 2023]
    p3_pf = (p3[p3["pnl_atr"] > 0]["pnl_atr"].sum() /
             -p3[p3["pnl_atr"] <= 0]["pnl_atr"].sum()) if len(p3[p3["pnl_atr"] <= 0]) > 0 and p3[p3["pnl_atr"] <= 0]["pnl_atr"].sum() < 0 else None
    return {
        "n": int(n_t), "wr": float(wr), "pf": float(pf),
        "expectancy_atr": float(expectancy),
        "p3_n": int(len(p3)), "p3_pf": p3_pf,
    }


def main():
    print("[G2] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df = df.dropna(subset=["atr14"])

    print("[G2] Detecting pivots (5-5)...")
    pivot_highs_55, pivot_lows_55 = detect_pivots(df, n_left=5, n_right=5)
    print(f"  pivot highs (5-5): {len(pivot_highs_55):,}")
    print(f"  pivot lows  (5-5): {len(pivot_lows_55):,}")

    # Build pivot price arrays for fast lookup
    # last_pivot_high_price[t] = price of most recent confirmed pivot high before bar t
    n = len(df)
    last_ph = np.full(n, np.nan)
    last_pl = np.full(n, np.nan)
    ph_pointer = 0
    pl_pointer = 0
    for t in range(n):
        # Advance pointer while pivot.confirmed_bar <= t
        while ph_pointer < len(pivot_highs_55) and pivot_highs_55[ph_pointer][2] <= t:
            last_ph[t] = pivot_highs_55[ph_pointer][1]
            ph_pointer += 1
        if t > 0 and np.isnan(last_ph[t]):
            last_ph[t] = last_ph[t - 1]

        while pl_pointer < len(pivot_lows_55) and pivot_lows_55[pl_pointer][2] <= t:
            last_pl[t] = pivot_lows_55[pl_pointer][1]
            pl_pointer += 1
        if t > 0 and np.isnan(last_pl[t]):
            last_pl[t] = last_pl[t - 1]

    df["last_pivot_high"] = last_ph
    df["last_pivot_low"] = last_pl
    df["broke_pivot_high"] = df["high"] > df["last_pivot_high"]
    df["broke_pivot_low"] = df["low"] < df["last_pivot_low"]

    # KST hour
    kst_idx = to_kst(df.index)
    valid = ~kst_idx.isna()
    df_use = df.loc[valid].copy()
    df_use["kst_hour"] = kst_idx[valid].hour

    print(f"  bars after KST conversion: {len(df_use):,}")

    all_results = {}

    for round_step in [100, 250, 500, 1000]:
        print(f"\n[G2] === Round step = {round_step} ===")
        events = detect_crosses_v2(df_use, round_step)
        print(f"  Total cross events: {len(events):,}")

        if len(events) == 0: continue

        # Add pivot break flags
        events["broke_pivot_high"] = events["idx"].apply(lambda i: bool(df_use["broke_pivot_high"].iloc[i]))
        events["broke_pivot_low"] = events["idx"].apply(lambda i: bool(df_use["broke_pivot_low"].iloc[i]))
        events["kst_hour"] = events["idx"].apply(lambda i: int(df_use["kst_hour"].iloc[i]))
        events["datetime"] = events["idx"].apply(lambda i: df_use.index[i])

        # Forward measurement (entry @ next open)
        forward = measure_forward_with_entry(df_use, events, fwd_bars=24)
        print(f"  Valid forward events: {len(forward):,}")

        # Categories
        forward["bp_high"] = forward["idx"].apply(lambda i: bool(df_use["broke_pivot_high"].iloc[i]))
        forward["bp_low"] = forward["idx"].apply(lambda i: bool(df_use["broke_pivot_low"].iloc[i]))
        forward["kst_hour"] = forward["idx"].apply(lambda i: int(df_use["kst_hour"].iloc[i]))

        groups = {
            "all_up":           forward[forward["direction"] == "up"],
            "all_down":         forward[forward["direction"] == "down"],
            "up_+pivotHigh":    forward[(forward["direction"] == "up") & forward["bp_high"]],
            "down_+pivotLow":   forward[(forward["direction"] == "down") & forward["bp_low"]],
            "up_NOTpivotHigh":  forward[(forward["direction"] == "up") & (~forward["bp_high"])],
            "down_NOTpivotLow": forward[(forward["direction"] == "down") & (~forward["bp_low"])],
        }

        round_results = {"round_step": round_step}
        for gname, gdf in groups.items():
            stats = stats_summary(gdf)
            round_results[gname] = stats

        # Print
        print(f"\n  {'Group':22s} {'N':>6s} {'sgn h2y(post)':>15s} {'sgn l2y':>10s} {'P3 sgn':>10s} {'P3 N':>6s}")
        for gname, stats in round_results.items():
            if gname == "round_step" or stats is None: continue
            h = stats["w_h2y"]
            l = stats["last_2y"]
            p3 = stats.get("by_period", {}).get("P3_2023+", {})
            p3_sgn = p3.get("mu_signed_post_cost", None)
            p3_n = p3.get("n", 0)
            print(f"  {gname:22s} {stats['n']:>6d} {h['mu_signed_post_cost']:>+15.4f} {l['mu_signed_post_cost']:>+10.4f} "
                  f"{(p3_sgn if p3_sgn is not None else 0):>+10.4f} {p3_n:>6d}")

        # Trade sim for top groups (down_+pivotLow LONG, up_+pivotHigh SHORT)
        if len(groups["down_+pivotLow"]) >= 50:
            sim_long = trade_sim_simple(df_use, groups["down_+pivotLow"], "long")
            round_results["trade_sim_down_PL_LONG"] = sim_long
            print(f"  TradeSim LONG (down+PL):  PF={sim_long['pf']:.3f} P3 PF={sim_long['p3_pf']} N={sim_long['n']} P3 N={sim_long['p3_n']}")
        if len(groups["up_+pivotHigh"]) >= 50:
            sim_short = trade_sim_simple(df_use, groups["up_+pivotHigh"], "short")
            round_results["trade_sim_up_PH_SHORT"] = sim_short
            print(f"  TradeSim SHORT (up+PH):   PF={sim_short['pf']:.3f} P3 PF={sim_short['p3_pf']} N={sim_short['n']} P3 N={sim_short['p3_n']}")

        all_results[f"R{round_step}"] = round_results

    # ===== Confluence: KST hour × R1000 down + PL =====
    print("\n[G2] === CONFLUENCE: KST hour × R1000 down + PL ===")
    conf_data = {}
    if "R1000" in all_results:
        # Re-detect to get raw events
        evs_1000 = detect_crosses_v2(df_use, 1000)
        evs_1000["broke_pivot_low"] = evs_1000["idx"].apply(lambda i: bool(df_use["broke_pivot_low"].iloc[i]))
        evs_1000["kst_hour"] = evs_1000["idx"].apply(lambda i: int(df_use["kst_hour"].iloc[i]))
        evs_1000["datetime"] = evs_1000["idx"].apply(lambda i: df_use.index[i])
        evs_filter = evs_1000[(evs_1000["direction"] == "down") & (evs_1000["broke_pivot_low"])]
        forward_1000 = measure_forward_with_entry(df_use, evs_filter, fwd_bars=24)
        forward_1000["kst_hour"] = forward_1000["idx"].apply(lambda i: int(df_use["kst_hour"].iloc[i]))
        print(f"\n  {'KST h':>6s} {'N':>4s} {'sgn h2y':>10s} {'sgn l2y':>10s}")
        for h in range(24):
            sub = forward_1000[forward_1000["kst_hour"] == h]
            if len(sub) < 10: continue
            stats = stats_summary(sub)
            if stats is None: continue
            hh = stats["w_h2y"]
            ll = stats["last_2y"]
            print(f"  {h:>6d} {stats['n']:>4d} {hh['mu_signed_post_cost']:>+10.4f} {ll['mu_signed_post_cost']:>+10.4f}")
            conf_data[f"hour_{h}"] = {"n": stats["n"], "h2y": hh["mu_signed_post_cost"], "l2y": ll["mu_signed_post_cost"]}
    all_results["confluence_R1000_down_PL_x_kst"] = conf_data

    # ===== Failed breakout: round break + reverse within 3 bars =====
    print("\n[G2] === Failed Breakout (R1000 up break + reverse in 3 bars) ===")
    if "R1000" in all_results:
        evs_1000_up = detect_crosses_v2(df_use, 1000)
        evs_1000_up = evs_1000_up[evs_1000_up["direction"] == "up"].copy()
        evs_1000_up["datetime"] = evs_1000_up["idx"].apply(lambda i: df_use.index[i])

        # Failed = within 3 bars after, low goes back below round_value
        rows = []
        low_arr = df_use["low"].values
        atr_arr = df_use["atr14"].values
        open_arr = df_use["open"].values
        close_arr = df_use["close"].values
        n = len(df_use)
        for _, ev in evs_1000_up.iterrows():
            idx = int(ev["idx"])
            if idx + 4 >= n: continue
            rv = float(ev["round_value"])
            failed = False
            for k in range(1, 4):
                if low_arr[idx + k] < rv:
                    failed = True
                    break
            if failed and idx + 27 < n:
                atr_i = atr_arr[idx]
                if atr_i <= 0: continue
                # Forward 24b after failure trigger (idx+k where break confirmed)
                entry = open_arr[idx + 4]
                fc = close_arr[idx + 4 + 24]
                fl = low_arr[idx + 4: idx + 4 + 24].min()
                fh = max(open_arr[idx+4], close_arr[idx+4: idx+4+24].max())
                signed = (fc - entry) / atr_i - COST_ATR
                rev_mfe = (entry - fl) / atr_i
                rows.append({
                    "idx": idx, "datetime": ev["datetime"],
                    "signed_atr": signed,
                    "signed_pre_cost": signed + COST_ATR,
                    "rev_mfe_atr": rev_mfe,
                    "cont_mfe_atr": (fh - entry) / atr_i,
                    "direction": "up_failed",
                })
        if rows:
            failed_df = pd.DataFrame(rows)
            stats = stats_summary(failed_df)
            print(f"  Failed R1000 up breakout: N={stats['n']} signed_h2y={stats['w_h2y']['mu_signed_post_cost']:+.4f} l2y={stats['last_2y']['mu_signed_post_cost']:+.4f}")
            all_results["failed_R1000_up"] = stats

    # Save
    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[G2] Saved → {OUT_DIR / 'results.json'}")
    return all_results


if __name__ == "__main__":
    main()
