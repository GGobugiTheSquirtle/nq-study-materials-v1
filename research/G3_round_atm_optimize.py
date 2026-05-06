"""Phase G3 — R500 up + 전고점 break SHORT × HE-001 ATM v2 grid

Goal: G2 발견된 R500 up+PH SHORT distribution edge (-0.127 ATR) 가
      HE-001 방식 (tight SL + Trail) 으로 trade-able 한지 확인.

Grid:
  SL_atr:        {0.3, 0.5, 0.75, 1.0, 1.25, 1.5}
  pre_trail_atr: {0.2, 0.3, 0.5, 0.7}
  trail_dist:    {0.2, 0.3, 0.5}
  max_hold:      {12, 24, 36, 48}

Trigger: R500 up-cross + pivot high (5-5) break, 5m TF
Direction: SHORT (mean revert from round resistance)
Cost: 0.022 ATR/RT
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from itertools import product
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators

OUT_DIR = Path(__file__).parent / "results" / "G3_round_atm"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COST_ATR = 0.022
ROUND_STEP = 500


def detect_pivots(df, n_left=5, n_right=5):
    high = df["high"].values
    low = df["low"].values
    n = len(df)
    pivot_highs, pivot_lows = [], []
    for t in range(n_left + n_right, n):
        i = t - n_right
        if i < n_left: continue
        wh = high[i - n_left: i + n_right + 1]
        if high[i] == wh.max():
            pivot_highs.append((i, high[i], t))
        wl = low[i - n_left: i + n_right + 1]
        if low[i] == wl.min():
            pivot_lows.append((i, low[i], t))
    return pivot_highs, pivot_lows


def build_last_pivot_arr(df, pivots, kind="high"):
    """Build last confirmed pivot price array."""
    n = len(df)
    arr = np.full(n, np.nan)
    ptr = 0
    last_val = np.nan
    for t in range(n):
        while ptr < len(pivots) and pivots[ptr][2] <= t:
            last_val = pivots[ptr][1]
            ptr += 1
        arr[t] = last_val
    return arr


def detect_signal_events(df_use, round_step=500):
    """R500 up + pivot high break events."""
    close = df_use["close"].values
    high = df_use["high"].values
    last_ph = df_use["last_pivot_high"].values
    n = len(df_use)
    events = []
    for i in range(1, n):
        prev_c = close[i - 1]
        r_above = (np.floor(prev_c / round_step) + 1) * round_step
        if r_above <= high[i]:
            # Up-cross occurred
            ph = last_ph[i]
            if not np.isnan(ph) and high[i] > ph:
                # Pivot high also broken
                events.append({
                    "idx": i,
                    "datetime": df_use.index[i],
                    "round_value": float(r_above),
                    "pivot_high": float(ph),
                })
    return pd.DataFrame(events)


def simulate_atm_short(open_, high, low, atr, datetimes, trigger_idx,
                       sl_atr, pre_trail_atr, trail_dist_atr, max_hold_bars):
    n = len(open_)
    rows = []
    for ti in trigger_idx:
        if ti + 1 + max_hold_bars >= n: continue
        entry = open_[ti + 1]
        cur_atr = atr[ti]
        if cur_atr <= 0 or np.isnan(cur_atr): continue
        sl = entry + sl_atr * cur_atr           # SHORT: SL above entry
        trail_trigger = entry - pre_trail_atr * cur_atr   # SHORT: profit when price down
        trail_dist = trail_dist_atr * cur_atr
        min_low_so_far = entry
        trail_active = False
        hit = "time"
        exit_p = None
        for k in range(1, max_hold_bars + 1):
            j = ti + 1 + k
            h, l = high[j], low[j]
            if l < min_low_so_far:
                min_low_so_far = l
            if not trail_active and l <= trail_trigger:
                trail_active = True
            if trail_active:
                new_sl = min_low_so_far + trail_dist
                if new_sl < sl:
                    sl = new_sl
            # Path-sim SL-first (SHORT: SL hit if h >= sl)
            if h >= sl:
                exit_p = sl
                hit = "trail" if trail_active else "sl"
                break
        if exit_p is None:
            exit_p = open_[ti + 1 + max_hold_bars]
        pnl_pre = (entry - exit_p) / cur_atr   # SHORT
        pnl = pnl_pre - COST_ATR
        rows.append({
            "idx": int(ti), "datetime": datetimes[ti],
            "entry": entry, "exit": exit_p, "atr": cur_atr,
            "hit": hit, "pnl_atr": pnl, "pnl_pre_cost": pnl_pre,
            "hold": k, "trail_active": trail_active,
        })
    return pd.DataFrame(rows)


def stats_summary(trades):
    if len(trades) == 0: return None
    wins = trades[trades["pnl_atr"] > 0]
    losses = trades[trades["pnl_atr"] <= 0]
    n = len(trades)
    pf = wins["pnl_atr"].sum() / -losses["pnl_atr"].sum() if losses["pnl_atr"].sum() < 0 else float("inf")
    wr = len(wins) / n
    expectancy = trades["pnl_atr"].mean()
    sharpe = expectancy / trades["pnl_atr"].std() * np.sqrt(252) if trades["pnl_atr"].std() > 0 else 0
    cum = trades["pnl_atr"].cumsum()
    peak = cum.cummax()
    mdd = (cum - peak).min()
    return {
        "n": int(n), "wr": float(wr), "pf": float(pf),
        "expectancy": float(expectancy),
        "sharpe_ann_proxy": float(sharpe),
        "total_pnl": float(trades["pnl_atr"].sum()),
        "mdd": float(mdd),
    }


def split_period(trades):
    if len(trades) == 0: return {}
    t = trades.copy()
    t["dt"] = pd.to_datetime(t["datetime"])
    t["period"] = "P3_2023+"
    t.loc[t["dt"].dt.year <= 2019, "period"] = "P1_2016_2019"
    t.loc[(t["dt"].dt.year >= 2020) & (t["dt"].dt.year <= 2022), "period"] = "P2_2020_2022"
    out = {}
    for p in ["P1_2016_2019", "P2_2020_2022", "P3_2023+"]:
        sub = t[t["period"] == p]
        out[p] = stats_summary(sub) if len(sub) > 0 else None
    return out


def main():
    print("[G3] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df = df.dropna(subset=["atr14"])

    print("[G3] Detecting pivots (5-5)...")
    pivot_highs, pivot_lows = detect_pivots(df, 5, 5)
    last_ph = build_last_pivot_arr(df, pivot_highs, "high")
    df["last_pivot_high"] = last_ph

    # KST conversion (filter valid)
    kst_idx = (df.index.tz_localize("America/New_York", nonexistent="shift_forward", ambiguous="NaT")
                  .tz_convert("Asia/Seoul"))
    valid = ~kst_idx.isna()
    df_use = df.loc[valid].copy()

    print("[G3] Detecting R500 up + PH break events...")
    events = detect_signal_events(df_use, ROUND_STEP)
    print(f"  Total events: {len(events):,}")

    if len(events) < 50:
        print("Insufficient events. Aborting.")
        return

    # Reset index for sim
    df_sim = df_use.reset_index().rename(columns={"datetime": "datetime"})
    df_sim["row_idx"] = np.arange(len(df_sim))

    open_ = df_sim["open"].values
    high  = df_sim["high"].values
    low   = df_sim["low"].values
    atr   = df_sim["atr14"].values
    dts   = df_sim["datetime"].values

    # Map event idx (from df_use) to row_idx in df_sim (same since both KST-filtered)
    trigger_idx = events["idx"].values

    # Grid
    sl_grid    = [0.3, 0.5, 0.75, 1.0, 1.25, 1.5]
    pt_grid    = [0.2, 0.3, 0.5, 0.7]
    td_grid    = [0.2, 0.3, 0.5]
    hold_grid  = [12, 24, 36, 48]

    print(f"[G3] Grid: {len(sl_grid)*len(pt_grid)*len(td_grid)*len(hold_grid)} combos")

    all_results = {}
    counter = 0
    for sl_a, pt_a, td_a, mh in product(sl_grid, pt_grid, td_grid, hold_grid):
        counter += 1
        if counter % 30 == 0:
            print(f"  [{counter}] running...")
        trades = simulate_atm_short(open_, high, low, atr, dts, trigger_idx, sl_a, pt_a, td_a, mh)
        if len(trades) == 0: continue
        stats = stats_summary(trades)
        period_stats = split_period(trades)
        key = f"SL{sl_a}_PT{pt_a}_TD{td_a}_H{mh}"
        all_results[key] = {
            "params": {"sl_atr": sl_a, "pre_trail_atr": pt_a, "trail_dist_atr": td_a, "max_hold_bars": mh},
            "total": stats,
            "by_period": period_stats,
        }

    # Rank by P3 PF (filter N>= some min)
    rankable = []
    for key, res in all_results.items():
        p3 = res["by_period"].get("P3_2023+")
        if p3 and p3["n"] >= 100:
            rankable.append((key, res, p3))
    rankable.sort(key=lambda x: -(x[2]["pf"] or 0))

    print(f"\n[G3] === TOP 15 by P3 PF (R500 up+PH SHORT, ATM grid) ===")
    print(f"{'Rank':>4s} {'Key':35s} {'PF':>6s} {'P3 PF':>7s} {'WR':>6s} {'Exp':>8s} {'P3 N':>5s}")
    for i, (k, res, p3) in enumerate(rankable[:15], 1):
        total_pf = res["total"]["pf"]
        flag = " ⭐" if p3["pf"] >= 1.10 else (" ✓" if p3["pf"] >= 1.0 else "")
        print(f"{i:>4d} {k[:35]:35s} {total_pf:>6.3f} {p3['pf']:>7.3f} {p3['wr']*100:>5.1f}% {p3['expectancy']:>+8.4f} {p3['n']:>5d}{flag}")

    # Best per SL summary
    print(f"\n[G3] === Best Per SL ===")
    for sl in sl_grid:
        sl_results = [(k, r) for k, r in all_results.items() if k.startswith(f"SL{sl}_")]
        sl_results.sort(key=lambda x: -(x[1]["by_period"].get("P3_2023+", {}).get("pf", 0) if x[1]["by_period"].get("P3_2023+") else 0))
        if sl_results:
            best_k, best_r = sl_results[0]
            p3 = best_r["by_period"].get("P3_2023+")
            if p3:
                print(f"  SL={sl}: best = {best_k}, P3 PF={p3['pf']:.3f}, N={p3['n']}, params={best_r['params']}")

    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[G3] Saved → {OUT_DIR / 'results.json'} ({len(all_results)} combos)")


if __name__ == "__main__":
    main()
