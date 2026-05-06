"""Phase E: Top edges 실전 조건 검증

Top edges from D1-D6:
  E_KST04_LONG (BURN_X), E_KST04_GUARD (z squeeze skip)
  E_KST14_LONG, E_KST19_LONG (NEW), E_KST15_LONG
  E_KST20_SHORT, E_KST21_SHORT, E_KST22_SHORT (BURN_R)
  E_MON_LONG, E_TUE_SHORT
  E_SQUEEZE12_LONG (any direction = LONG bias signed_h2y +0.05)
  E_BULL_BODY_CONT, E_BEAR_BODY_CONT
  E_CONF_KST14MON, E_CONF_KST21TUE, E_CONF_SQ12MON

For each edge:
  - Identify trigger bars (signal points)
  - Simulate trade: entry at next bar open, SL = 1.5×ATR, TP grid {1, 1.5, 2, 3}×ATR
  - Path-sim SL-first ordering
  - Cost: commission RT $2.18 + slippage 0.03% one-way (= 0.06% RT roughly)
    NQ point value $20/pt, 1 ATR ≈ 15 pt average → $300/contract per ATR
    Cost as ATR equiv: $2.18 + $4.5 slip = ~$6.7 / $300 = 0.022 ATR
  - Compute: WR, expectancy, PF, Sharpe, by regime, by period

Periods:
  P1: 2016-2019 (early)
  P2: 2020-2022 (covid + bear)
  P3: 2023-2026 (recent)

Regime: BULL / BEAR / CHOP (from regime_label)
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from pathlib import Path
from _lib.data_loader import load_nq
from _lib.indicators import add_indicators, regime_label

OUT_DIR = Path(__file__).parent / "results" / "E_edge_validation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Cost in ATR units (rough): $6.7 per RT / $300 ATR ≈ 0.022 ATR per round trip
COST_ATR = 0.022


def to_kst(idx):
    return (idx.tz_localize("America/New_York", nonexistent="shift_forward", ambiguous="NaT")
              .tz_convert("Asia/Seoul"))


def simulate_trades(df: pd.DataFrame, trigger_idx: np.ndarray, direction: str,
                    sl_atr: float = 1.5, tp_atrs=(1.0, 1.5, 2.0, 3.0),
                    max_hold_bars: int = 48):
    """Simulate trade: entry at next bar open, SL=sl_atr, TP grid.
    df has 'datetime' column (after reset_index).
    """
    high = df["high"].values
    low = df["low"].values
    open_ = df["open"].values
    atr = df["atr14"].values
    datetimes = df["datetime"].values
    n = len(df)
    sign = +1 if direction == "long" else -1

    results_per_tp = {}
    for tp_atr in tp_atrs:
        rows = []
        for ti in trigger_idx:
            if ti + 1 + max_hold_bars >= n:
                continue
            entry = open_[ti + 1]
            cur_atr = atr[ti]
            if cur_atr <= 0 or np.isnan(cur_atr):
                continue
            sl = entry - sign * sl_atr * cur_atr
            tp = entry + sign * tp_atr * cur_atr
            hit = "time"
            exit_price = open_[ti + 1 + max_hold_bars]
            for k in range(1, max_hold_bars + 1):
                idx = ti + 1 + k
                if idx >= n:
                    break
                h, l = high[idx], low[idx]
                if direction == "long":
                    if l <= sl:
                        exit_price = sl
                        hit = "sl"
                        break
                    if h >= tp:
                        exit_price = tp
                        hit = "tp"
                        break
                else:
                    if h >= sl:
                        exit_price = sl
                        hit = "sl"
                        break
                    if l <= tp:
                        exit_price = tp
                        hit = "tp"
                        break
            pnl_pre = sign * (exit_price - entry) / cur_atr
            pnl_atr = pnl_pre - COST_ATR
            rows.append({"idx": int(ti), "entry": entry, "exit": exit_price,
                         "atr": cur_atr, "hit": hit, "pnl_atr": pnl_atr,
                         "pnl_pre_cost": pnl_pre, "hold": k,
                         "datetime": datetimes[ti]})
        df_r = pd.DataFrame(rows)
        results_per_tp[f"tp_{tp_atr}"] = df_r
    return results_per_tp


def stats_summary(trades: pd.DataFrame):
    """Compute WR / PF / expectancy / Sharpe."""
    if len(trades) == 0:
        return {}
    wins = trades[trades["pnl_atr"] > 0]
    losses = trades[trades["pnl_atr"] <= 0]
    n = len(trades)
    n_wins = len(wins)
    n_losses = len(losses)
    wr = n_wins / n if n else 0
    avg_win = wins["pnl_atr"].mean() if n_wins else 0
    avg_loss = losses["pnl_atr"].mean() if n_losses else 0
    pf = wins["pnl_atr"].sum() / -losses["pnl_atr"].sum() if losses["pnl_atr"].sum() < 0 else float("inf")
    expectancy = trades["pnl_atr"].mean()
    sharpe = expectancy / trades["pnl_atr"].std() * np.sqrt(252) if trades["pnl_atr"].std() > 0 else 0
    # Cumulative drawdown
    cum = trades["pnl_atr"].cumsum()
    peak = cum.cummax()
    dd = cum - peak
    mdd = dd.min()
    return {
        "n": int(n),
        "wr": float(wr),
        "avg_win_atr": float(avg_win),
        "avg_loss_atr": float(avg_loss),
        "pf": float(pf),
        "expectancy_atr": float(expectancy),
        "sharpe_ann_proxy": float(sharpe),
        "total_pnl_atr": float(trades["pnl_atr"].sum()),
        "mdd_atr": float(mdd),
        "max_consec_loss": int(_max_consec_loss(trades)),
    }


def _max_consec_loss(trades):
    losses_streak = 0
    max_streak = 0
    for v in trades["pnl_atr"]:
        if v <= 0:
            losses_streak += 1
            max_streak = max(max_streak, losses_streak)
        else:
            losses_streak = 0
    return max_streak


def regime_period_breakdown(trades: pd.DataFrame, df_full: pd.DataFrame, dt_to_period_func):
    """Breakdown by regime + period."""
    out = {"by_regime": {}, "by_period": {}}
    if len(trades) == 0:
        return out

    # Map trade idx → regime
    regimes = df_full["regime"].values
    trades = trades.copy()
    trades["regime"] = trades["idx"].apply(lambda i: regimes[i] if i < len(regimes) else "?")
    trades["period"] = trades["datetime"].apply(dt_to_period_func)

    for reg in ["BULL", "BEAR", "CHOP"]:
        sub = trades[trades["regime"] == reg]
        out["by_regime"][reg] = stats_summary(sub)

    for per in ["P1_2016_2019", "P2_2020_2022", "P3_2023_2026"]:
        sub = trades[trades["period"] == per]
        out["by_period"][per] = stats_summary(sub)

    return out


def _period_label(dt):
    if not hasattr(dt, "year"):
        dt = pd.to_datetime(dt)
    y = dt.year
    if y <= 2019: return "P1_2016_2019"
    if y <= 2022: return "P2_2020_2022"
    return "P3_2023_2026"


def main():
    print("[E] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df["regime"] = regime_label(df)

    # ATR z 60-day
    atr_lookback = 60 * 24 * 12
    df["atr_mean60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).mean()
    df["atr_std60d"] = df["atr14"].rolling(window=atr_lookback, min_periods=1000).std()
    df["atr_z"] = (df["atr14"] - df["atr_mean60d"]) / df["atr_std60d"]
    df["squeeze_12"] = df["atr_z"].rolling(12).max() < -0.5

    # Candle structure
    body = df["close"] - df["open"]
    range_ = (df["high"] - df["low"]).replace(0, np.nan)
    df["body_pct"] = body.abs() / range_
    df["body_dir"] = np.sign(body)
    df["bull_strong"] = (df["body_pct"] >= 0.7) & (df["body_dir"] > 0)
    df["bear_strong"] = (df["body_pct"] >= 0.7) & (df["body_dir"] < 0)

    df = df.dropna(subset=["atr14", "atr_z"]).copy()

    # KST conversion
    print("[E] Converting to KST...")
    kst_idx = to_kst(df.index)
    valid = ~kst_idx.isna()
    df = df.loc[valid].copy()
    df["kst_hour"] = kst_idx[valid].hour
    df["kst_dow"] = kst_idx[valid].dayofweek

    # Reset to integer index for trade simulation
    df = df.reset_index().rename(columns={"datetime": "datetime"})
    df.set_index("datetime", inplace=True)
    df_idx = np.arange(len(df))
    df["row_idx"] = df_idx

    print(f"  total bars: {len(df):,}")

    # Define edges (signal mask, direction, name)
    edges = [
        # Single-factor LONG
        ("KST04_LONG_BURN_X", df["kst_hour"] == 4, "long"),
        ("KST14_LONG_USlunch", df["kst_hour"] == 14, "long"),
        ("KST19_LONG_preNY", df["kst_hour"] == 19, "long"),
        ("KST15_LONG_EUclose", df["kst_hour"] == 15, "long"),
        # Single-factor SHORT
        ("KST20_SHORT", df["kst_hour"] == 20, "short"),
        ("KST21_SHORT", df["kst_hour"] == 21, "short"),
        ("KST22_SHORT_BURN_R", df["kst_hour"] == 22, "short"),
        # Day of week
        ("MON_LONG", df["kst_dow"] == 0, "long"),
        ("TUE_SHORT", df["kst_dow"] == 1, "short"),
        # Squeeze
        ("SQUEEZE12_LONG", df["squeeze_12"], "long"),
        # Body continuation
        ("BULL_BODY_CONT_LONG", df["bull_strong"], "long"),
        ("BEAR_BODY_CONT_SHORT", df["bear_strong"], "short"),
        # Confluences
        ("CONF_KST14_MON_LONG", (df["kst_hour"] == 14) & (df["kst_dow"] == 0), "long"),
        ("CONF_KST21_TUE_SHORT", (df["kst_hour"] == 21) & (df["kst_dow"] == 1), "short"),
        ("CONF_SQ12_MON_LONG", df["squeeze_12"] & (df["kst_dow"] == 0), "long"),
        ("CONF_KST04_NO_SQUEEZE_LONG", (df["kst_hour"] == 4) & (~df["squeeze_12"]), "long"),
        ("GUARD_KST04_SQUEEZE_LONG", (df["kst_hour"] == 4) & (df["squeeze_12"]), "long"),
        ("GUARD_KST04_SQUEEZE_SHORT", (df["kst_hour"] == 4) & (df["squeeze_12"]), "short"),
        # KST 19 confluences
        ("CONF_KST19_MON_LONG", (df["kst_hour"] == 19) & (df["kst_dow"] == 0), "long"),
        ("CONF_KST19_BULL_BODY_LONG", (df["kst_hour"] == 19) & df["bull_strong"], "long"),
    ]

    # Reset index back to int for sim
    df_sim = df.reset_index()

    all_results = {}
    print(f"\n[E] === Cost-adjusted trade sim (cost = {COST_ATR:.3f} ATR per round-trip) ===")

    for name, mask, direction in edges:
        # Trigger only at the first bar of that hour (avoid overlapping signals from same hour)
        # For simplicity: all signal bars are triggers (trade entry next bar)
        # But cap total triggers to keep tractable + avoid overlap by sampling 1-per-hour
        if "kst_hour" in name.lower() or "KST" in name:
            # Take first bar of each hour where mask True
            df_sig = df_sim.loc[mask.values].copy()
            df_sig["hour_floor"] = pd.to_datetime(df_sig["datetime"]).dt.floor("h")
            df_sig = df_sig.drop_duplicates(subset="hour_floor", keep="first")
            trigger_idx = df_sig["row_idx"].values
        else:
            # Other signals: sample at most every 12 bars (1 hour) to avoid clustering
            sig_rows = df_sim.loc[mask.values]
            trigger_idx = sig_rows["row_idx"].values
            if len(trigger_idx) > 30000:
                # downsample stratified
                trigger_idx = trigger_idx[::max(1, len(trigger_idx) // 30000)]

        if len(trigger_idx) < 50:
            print(f"  {name}: SKIP (N={len(trigger_idx)})")
            continue

        # Simulate
        results_per_tp = simulate_trades(df_sim, trigger_idx, direction,
                                          sl_atr=1.5, tp_atrs=(1.0, 1.5, 2.0, 3.0),
                                          max_hold_bars=48)
        # Stats per TP
        edge_result = {"direction": direction, "n_triggers": int(len(trigger_idx)), "tp_results": {}}
        for tp_key, trades in results_per_tp.items():
            stats = stats_summary(trades)
            breakdown = regime_period_breakdown(trades, df_sim, _period_label)
            edge_result["tp_results"][tp_key] = {**stats, "breakdown": breakdown}

        all_results[name] = edge_result

    # Print summary table
    print(f"\n{'Edge':35s} {'N':>5s} {'TP':>6s} {'WR':>6s} {'PF':>6s} {'Exp':>8s} {'P3 PF':>7s} {'P3 N':>5s}")
    for name, res in all_results.items():
        for tp_key in ["tp_1.0", "tp_1.5", "tp_2.0"]:
            r = res["tp_results"][tp_key]
            p3 = r.get("breakdown", {}).get("by_period", {}).get("P3_2023_2026", {})
            line = f"{name:35s} {r['n']:>5d} {tp_key:>6s} {r['wr']*100:>5.1f}% {r['pf']:>6.2f} {r['expectancy_atr']:>+8.4f} {p3.get('pf', 0):>7.2f} {p3.get('n', 0):>5d}"
            print(line)
        print()

    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[E] Saved → {OUT_DIR / 'results.json'}")
    return all_results


if __name__ == "__main__":
    main()
