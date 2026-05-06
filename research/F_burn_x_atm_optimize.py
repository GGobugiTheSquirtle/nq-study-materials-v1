"""HE-001: BURN_X ATM 최적화 — SL ≤ 1.5×ATR 제약, Trail grid

Goal: KST 04:30 LONG entry. Find SL/Trail/Hold optimal that maximize
      P3 (recent) PF AND keeps SL not "지나치게 크지 않게" (≤ 1.5 ATR).

Grid:
  SL_atr:           {0.5, 0.75, 1.0, 1.25, 1.5}    (5)
  pre_trail_atr:    {0.3, 0.5, 0.7, 1.0}           (4)
  trail_dist_atr:   {0.3, 0.5, 0.7, 1.0}           (4)   - trail SL distance from current high
  max_hold_bars:    {12, 24, 36, 48, 60}           (5)
  squeeze_guard:    {True, False}                  (2)

Total combinations: 5×4×4×5×2 = 800

Cost: 0.022 ATR/RT.
Direction: LONG only (BURN_X).
Trigger: KST 04:30 first bar of hour.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from itertools import product
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators

OUT_DIR = Path(__file__).parent / "results" / "F_burn_x_atm"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COST_ATR = 0.022


def to_kst(idx):
    return (idx.tz_localize("America/New_York", nonexistent="shift_forward", ambiguous="NaT")
              .tz_convert("Asia/Seoul"))


def simulate_atm_long(open_, high, low, atr, datetimes, trigger_idx,
                      sl_atr, pre_trail_atr, trail_dist_atr, max_hold_bars):
    """Simulate LONG entry with trailing stop.

    Logic:
      Entry: open_[ti+1]
      Initial SL: entry - sl_atr × ATR
      Trail activation: when high reaches entry + pre_trail_atr × ATR
      After activation: SL = max(SL, max_high_so_far - trail_dist_atr × ATR)
      Exit: SL hit OR max_hold reached (close-out)
    """
    n = len(open_)
    rows = []
    for ti in trigger_idx:
        if ti + 1 + max_hold_bars >= n:
            continue
        entry = open_[ti + 1]
        cur_atr = atr[ti]
        if cur_atr <= 0 or np.isnan(cur_atr):
            continue
        sl = entry - sl_atr * cur_atr
        trail_trigger_price = entry + pre_trail_atr * cur_atr
        trail_dist = trail_dist_atr * cur_atr
        max_high_so_far = entry
        trail_active = False
        hit = "time"
        exit_price = None
        for k in range(1, max_hold_bars + 1):
            idx = ti + 1 + k
            h = high[idx]
            l = low[idx]
            # Update max high
            if h > max_high_so_far:
                max_high_so_far = h
            # Check trail activation
            if not trail_active and h >= trail_trigger_price:
                trail_active = True
            # Update trailing SL
            if trail_active:
                new_sl = max_high_so_far - trail_dist
                if new_sl > sl:
                    sl = new_sl
            # Check SL hit (path-sim: SL first if low <= sl)
            if l <= sl:
                exit_price = sl
                hit = "trail" if trail_active else "sl"
                break
        if exit_price is None:
            exit_price = open_[ti + 1 + max_hold_bars]
        pnl_pre = (exit_price - entry) / cur_atr
        pnl = pnl_pre - COST_ATR
        rows.append({"idx": int(ti), "datetime": datetimes[ti],
                     "entry": entry, "exit": exit_price, "atr": cur_atr,
                     "hit": hit, "pnl_atr": pnl, "pnl_pre_cost": pnl_pre,
                     "hold": k, "trail_active": trail_active})
    return pd.DataFrame(rows)


def stats_summary(trades: pd.DataFrame):
    if len(trades) == 0:
        return {}
    wins = trades[trades["pnl_atr"] > 0]
    losses = trades[trades["pnl_atr"] <= 0]
    n = len(trades)
    n_wins = len(wins)
    wr = n_wins / n if n else 0
    avg_win = wins["pnl_atr"].mean() if n_wins else 0
    avg_loss = losses["pnl_atr"].mean() if len(losses) else 0
    pf = wins["pnl_atr"].sum() / -losses["pnl_atr"].sum() if losses["pnl_atr"].sum() < 0 else float("inf")
    expectancy = trades["pnl_atr"].mean()
    sharpe = expectancy / trades["pnl_atr"].std() * np.sqrt(252) if trades["pnl_atr"].std() > 0 else 0
    cum = trades["pnl_atr"].cumsum()
    peak = cum.cummax()
    dd = cum - peak
    mdd = dd.min()
    sl_hit_count = (trades["hit"] == "sl").sum()
    trail_hit_count = (trades["hit"] == "trail").sum()
    time_count = (trades["hit"] == "time").sum()
    return {
        "n": int(n), "wr": float(wr), "pf": float(pf),
        "expectancy": float(expectancy),
        "avg_win": float(avg_win), "avg_loss": float(avg_loss),
        "sharpe_ann_proxy": float(sharpe),
        "total_pnl": float(trades["pnl_atr"].sum()),
        "mdd": float(mdd),
        "sl_hit_pct": float(sl_hit_count / n * 100),
        "trail_hit_pct": float(trail_hit_count / n * 100),
        "time_exit_pct": float(time_count / n * 100),
    }


def split_period(trades):
    if len(trades) == 0:
        return {}
    out = {}
    trades = trades.copy()
    trades["dt"] = pd.to_datetime(trades["datetime"])
    trades["period"] = "P3_2023+"
    trades.loc[trades["dt"].dt.year <= 2019, "period"] = "P1_2016_2019"
    trades.loc[(trades["dt"].dt.year >= 2020) & (trades["dt"].dt.year <= 2022), "period"] = "P2_2020_2022"
    for p in ["P1_2016_2019", "P2_2020_2022", "P3_2023+"]:
        out[p] = stats_summary(trades[trades["period"] == p])
    return out


def main():
    print("[F] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)

    # Squeeze indicator
    atr_lookback = 60 * 24 * 12
    df["atr_mean60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).mean()
    df["atr_std60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).std()
    df["atr_z"] = (df["atr14"] - df["atr_mean60d"]) / df["atr_std60d"]
    df["squeeze_12"] = df["atr_z"].rolling(12).max() < -0.5
    df = df.dropna(subset=["atr14", "atr_z"]).copy()

    # KST
    kst_idx = to_kst(df.index)
    valid = ~kst_idx.isna()
    df = df.loc[valid].copy()
    df["kst_hour"] = kst_idx[valid].hour

    # Reset index for sim
    df = df.reset_index().rename(columns={"datetime": "datetime"})
    df["row_idx"] = np.arange(len(df))

    # Identify KST 04 trigger bars (first bar per hour to avoid duplicates)
    df_04 = df[df["kst_hour"] == 4].copy()
    df_04["dt_floor"] = pd.to_datetime(df_04["datetime"]).dt.floor("h")
    df_04 = df_04.drop_duplicates(subset="dt_floor", keep="first")

    # Triggers — both no-guard and squeeze-guard
    triggers_no_guard = df_04["row_idx"].values
    triggers_with_guard = df_04[~df_04["squeeze_12"]]["row_idx"].values

    print(f"[F] KST 04 triggers: total={len(triggers_no_guard)}, no-squeeze={len(triggers_with_guard)}")

    open_ = df["open"].values
    high = df["high"].values
    low = df["low"].values
    atr_arr = df["atr14"].values
    dt_arr = df["datetime"].values

    # Grid
    sl_grid = [0.5, 0.75, 1.0, 1.25, 1.5]
    pre_trail_grid = [0.3, 0.5, 0.7, 1.0]
    trail_dist_grid = [0.3, 0.5, 0.7, 1.0]
    max_hold_grid = [12, 24, 36, 48, 60]
    guard_grid = [False, True]

    print(f"[F] Grid combos: {len(sl_grid)*len(pre_trail_grid)*len(trail_dist_grid)*len(max_hold_grid)*len(guard_grid)}")

    all_results = {}
    counter = 0
    for sl_atr, pre_trail_atr, trail_dist_atr, max_hold, use_guard in product(
        sl_grid, pre_trail_grid, trail_dist_grid, max_hold_grid, guard_grid
    ):
        counter += 1
        if counter % 50 == 0:
            print(f"  [{counter}] running...")
        triggers = triggers_with_guard if use_guard else triggers_no_guard
        trades = simulate_atm_long(open_, high, low, atr_arr, dt_arr, triggers,
                                    sl_atr, pre_trail_atr, trail_dist_atr, max_hold)
        if len(trades) == 0:
            continue
        stats = stats_summary(trades)
        period_stats = split_period(trades)
        key = f"SL{sl_atr}_PT{pre_trail_atr}_TD{trail_dist_atr}_H{max_hold}_G{int(use_guard)}"
        all_results[key] = {
            "params": {"sl_atr": sl_atr, "pre_trail_atr": pre_trail_atr,
                       "trail_dist_atr": trail_dist_atr, "max_hold_bars": max_hold,
                       "squeeze_guard": use_guard},
            "total": stats,
            "by_period": period_stats,
        }

    # Rank by P3 PF (with N >= 200 filter)
    rankable = []
    for key, res in all_results.items():
        p3 = res["by_period"].get("P3_2023+", {})
        if p3.get("n", 0) >= 200:
            rankable.append((key, res, p3))

    print(f"\n[F] Total combos with P3 N >= 200: {len(rankable)}")

    rankable.sort(key=lambda x: -x[2].get("pf", 0))
    print(f"\n[F] === TOP 20 by P3 PF ===")
    print(f"{'Rank':>4s} {'Key':50s} {'P3 PF':>6s} {'P3 WR':>6s} {'P3 Exp':>8s} {'P3 N':>5s} {'Total PF':>8s}")
    for i, (k, res, p3) in enumerate(rankable[:20], 1):
        total_pf = res["total"]["pf"]
        print(f"{i:>4d} {k[:50]:50s} {p3['pf']:>6.3f} {p3['wr']*100:>5.1f}% {p3['expectancy']:>+8.4f} {p3['n']:>5d} {total_pf:>8.3f}")

    print(f"\n[F] === TOP 10 by Sharpe (P3) ===")
    rankable.sort(key=lambda x: -x[2].get("sharpe_ann_proxy", 0))
    print(f"{'Rank':>4s} {'Key':50s} {'P3 Sharpe':>10s} {'P3 PF':>6s} {'P3 N':>5s}")
    for i, (k, res, p3) in enumerate(rankable[:10], 1):
        print(f"{i:>4d} {k[:50]:50s} {p3.get('sharpe_ann_proxy', 0):>10.3f} {p3['pf']:>6.3f} {p3['n']:>5d}")

    print(f"\n[F] === TOP 10 by P3 Total PnL (ATR) ===")
    rankable.sort(key=lambda x: -x[2].get("total_pnl", 0))
    print(f"{'Rank':>4s} {'Key':50s} {'P3 Total':>9s} {'P3 PF':>6s} {'P3 MDD':>8s} {'P3 N':>5s}")
    for i, (k, res, p3) in enumerate(rankable[:10], 1):
        print(f"{i:>4d} {k[:50]:50s} {p3.get('total_pnl', 0):>+9.3f} {p3['pf']:>6.3f} {p3.get('mdd', 0):>+8.3f} {p3['n']:>5d}")

    # Save
    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[F] Saved → {OUT_DIR / 'results.json'} ({len(all_results)} combos)")


if __name__ == "__main__":
    main()
