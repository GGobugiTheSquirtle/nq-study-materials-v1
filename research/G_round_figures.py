"""Phase G: Round figure breakouts research

Hypotheses:
  H1a: Round figure (100/500/1000) up-cross → forward signed return shows mean revert (SHORT bias)
  H1b: K-unit (1000) round figures show stronger effect than 100/500
  H1c: Round + recent swing high concurrent (전고점 + 라운드) → strongest mean revert

Method:
  - Detect cross events: prev_high < round_value AND high >= round_value (up-cross)
                         OR prev_low > round_value AND low <= round_value (down-cross)
  - Round levels tested: 50 / 100 / 250 / 500 / 1000 NQ points
  - Confluence variant: cross + concurrent swing high break (high > recent 50-bar high prev)
  - Forward measurements: 12/24/48 bar signed return + reversal MFE
  - Compared against baseline (random non-round bars)

Cost not applied (raw distribution analysis). If GO, follow-up trade sim.
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

OUT_DIR = Path(__file__).parent / "results" / "G_round_figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
SWING_LOOKBACK = 50    # "전고점" = 직전 50봉 high


def detect_crosses(df: pd.DataFrame, round_step: int) -> pd.DataFrame:
    """Detect round figure cross events.

    Up-cross: prev_high < round_value AND current high >= round_value
              (price 가 새 round figure 를 위로 돌파)
    Down-cross: prev_low > round_value AND current low <= round_value
    """
    high = df["high"].values
    low = df["low"].values
    n = len(df)

    events = []
    for i in range(1, n):
        # Up-cross
        # Find round value crossed
        prev_h = high[i - 1]
        cur_h = high[i]
        if cur_h > prev_h:
            # Find smallest round value > prev_h that <= cur_h
            r_low = (np.floor(prev_h / round_step) + 1) * round_step
            if r_low <= cur_h:
                # Cross occurred
                events.append({
                    "idx": i, "datetime": df.index[i],
                    "direction": "up",
                    "round_value": float(r_low),
                    "round_step": round_step,
                    "high": cur_h,
                    "atr": df["atr14"].iloc[i],
                })

        # Down-cross (down breakout)
        prev_l = low[i - 1]
        cur_l = low[i]
        if cur_l < prev_l:
            r_high = (np.ceil(prev_l / round_step) - 1) * round_step
            if r_high >= cur_l:
                events.append({
                    "idx": i, "datetime": df.index[i],
                    "direction": "down",
                    "round_value": float(r_high),
                    "round_step": round_step,
                    "low": cur_l,
                    "atr": df["atr14"].iloc[i],
                })

    return pd.DataFrame(events)


def add_swing_high_low_flags(df: pd.DataFrame, lookback: int = 50):
    """Add columns: 'broke_swing_high' / 'broke_swing_low' (current bar broke recent N-bar extreme)"""
    rolling_max = df["high"].rolling(lookback, min_periods=lookback).max().shift(1)
    rolling_min = df["low"].rolling(lookback, min_periods=lookback).min().shift(1)
    df["broke_swing_high"] = df["high"] > rolling_max
    df["broke_swing_low"] = df["low"] < rolling_min
    return df


def measure_forward(df: pd.DataFrame, events: pd.DataFrame, fwd_bars: int = 24):
    """For each event, compute forward signed return + reversal MFE."""
    high = df["high"].values
    low = df["low"].values
    close = df["close"].values
    n = len(df)

    rows = []
    for _, ev in events.iterrows():
        idx = int(ev["idx"])
        if idx + fwd_bars >= n:
            continue
        atr_i = ev["atr"]
        if atr_i <= 0 or np.isnan(atr_i):
            continue
        ref_price = close[idx]
        future_high = high[idx + 1: idx + 1 + fwd_bars].max()
        future_low = low[idx + 1: idx + 1 + fwd_bars].min()
        future_close = close[idx + fwd_bars]
        signed = (future_close - ref_price) / atr_i

        if ev["direction"] == "up":
            # Reversal = price comes back DOWN
            rev_mfe = (ref_price - future_low) / atr_i
            cont_mfe = (future_high - ref_price) / atr_i
        else:
            rev_mfe = (future_high - ref_price) / atr_i
            cont_mfe = (ref_price - future_low) / atr_i

        rows.append({
            "idx": idx, "datetime": ev["datetime"],
            "direction": ev["direction"],
            "round_step": ev["round_step"],
            "round_value": ev["round_value"],
            "atr": atr_i,
            "signed_atr": signed,
            "rev_mfe_atr": rev_mfe,
            "cont_mfe_atr": cont_mfe,
        })
    return pd.DataFrame(rows)


def report_one(name: str, df: pd.DataFrame, baseline_signed: float | None = None):
    """Generate summary stats for one event group."""
    if len(df) == 0:
        return {"name": name, "n": 0, "skip": True}
    times = pd.DatetimeIndex(df["datetime"])
    weights = get_all_weights(times)
    h2y = weights["w_h2y"]
    l2y = weights["last_2y"]
    eq  = weights["w_eq"]

    signed = df["signed_atr"].values
    rev_mfe = df["rev_mfe_atr"].values
    cont_mfe = df["cont_mfe_atr"].values

    out = {
        "name": name,
        "n": int(len(df)),
        "data_range": [str(df["datetime"].iloc[0]), str(df["datetime"].iloc[-1])],
        "by_scheme": {},
    }
    for sch_name, w in weights.items():
        out["by_scheme"][sch_name] = {
            "mu_signed": weighted_mean(signed, w),
            "mu_rev_mfe": weighted_mean(rev_mfe, w),
            "mu_cont_mfe": weighted_mean(cont_mfe, w),
        }
    return out


def main():
    print("[G] Loading NQ 5m...")
    df = load_nq("5m", start="2016-01-01")
    df = add_indicators(df)
    df = df.dropna(subset=["atr14"])
    df = add_swing_high_low_flags(df, lookback=SWING_LOOKBACK)

    # Reset index for sim use
    df_sim = df.reset_index()
    df_sim_idx = df.copy()    # keep DatetimeIndex for DateRange

    all_results = {}

    for round_step in [50, 100, 250, 500, 1000]:
        print(f"\n[G] === Round step = {round_step} ===")
        events = detect_crosses(df, round_step)
        print(f"  Total cross events: {len(events):,}")

        if len(events) == 0:
            continue

        # Add swing high/low flags from main df
        events["broke_swing_high"] = events["idx"].apply(
            lambda i: bool(df["broke_swing_high"].iloc[i]) if i < len(df) else False)
        events["broke_swing_low"] = events["idx"].apply(
            lambda i: bool(df["broke_swing_low"].iloc[i]) if i < len(df) else False)

        # Forward measurement (24b)
        forward = measure_forward(df, events, fwd_bars=24)

        # Direction split
        up_events = forward[forward["direction"] == "up"]
        down_events = forward[forward["direction"] == "down"]
        print(f"  Up-cross: {len(up_events):,}, Down-cross: {len(down_events):,}")

        # Add swing-high broken flag
        events_idx_set = events.set_index("idx")
        forward = forward.merge(events_idx_set[["broke_swing_high", "broke_swing_low"]],
                                left_on="idx", right_index=True, how="left")

        # Categories
        up_with_sh   = forward[(forward["direction"] == "up") & (forward["broke_swing_high"])]
        up_without   = forward[(forward["direction"] == "up") & (~forward["broke_swing_high"])]
        down_with_sl = forward[(forward["direction"] == "down") & (forward["broke_swing_low"])]
        down_without = forward[(forward["direction"] == "down") & (~forward["broke_swing_low"])]

        round_results = {
            "round_step": round_step,
            "n_total": int(len(forward)),
            "n_up": int(len(up_events)),
            "n_down": int(len(down_events)),
            "all_up": report_one(f"R{round_step}_up_all", up_events),
            "all_down": report_one(f"R{round_step}_down_all", down_events),
            "up_with_swing_high": report_one(f"R{round_step}_up_+SH", up_with_sh),
            "up_without_swing_high": report_one(f"R{round_step}_up_noSH", up_without),
            "down_with_swing_low": report_one(f"R{round_step}_down_+SL", down_with_sl),
            "down_without_swing_low": report_one(f"R{round_step}_down_noSL", down_without),
        }

        # Print summary
        print(f"\n  {'Group':32s} {'N':>6s} {'mu_sgn h2y':>12s} {'rev_mfe':>10s} {'cont_mfe':>10s} {'mu_sgn l2y':>12s}")
        for key in ["all_up", "all_down", "up_with_swing_high", "up_without_swing_high", "down_with_swing_low", "down_without_swing_low"]:
            r = round_results[key]
            if r.get("skip"):
                continue
            h = r["by_scheme"]["w_h2y"]
            l = r["by_scheme"]["last_2y"]
            print(f"  {key:32s} {r['n']:>6d} {h['mu_signed']:>+12.4f} {h['mu_rev_mfe']:>10.3f} {h['mu_cont_mfe']:>10.3f} {l['mu_signed']:>+12.4f}")

        all_results[f"R{round_step}"] = round_results

    # ===== Baseline: random non-round-cross bars =====
    print(f"\n[G] === BASELINE (random sample, all bars) ===")
    rng = np.random.default_rng(SEED)
    n_baseline = 30000
    bar_indices = rng.choice(len(df) - 50, size=n_baseline, replace=False)

    bl_events = pd.DataFrame({
        "idx": bar_indices,
        "datetime": df.index[bar_indices],
        "direction": "up",      # placeholder, signed return is direction-agnostic
        "round_value": np.nan,
        "round_step": 0,
        "atr": df["atr14"].iloc[bar_indices].values,
    })
    bl_forward = measure_forward(df, bl_events, fwd_bars=24)
    bl_report = report_one("baseline_random", bl_forward)
    all_results["baseline"] = bl_report

    h_bl = bl_report["by_scheme"]["w_h2y"]
    print(f"  baseline_random      {bl_report['n']:>6d}    mu_signed={h_bl['mu_signed']:+.4f} (random forward 24b)")

    # ===== Save =====
    with open(OUT_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n[G] Saved → {OUT_DIR / 'results.json'}")

    # ===== Final ranking — top mean-revert (large negative signed for up-cross) =====
    print("\n[G] === KEY FINDINGS — UP-CROSS mean revert ranking (h2y) ===")
    rows = []
    for rstep_key in ["R50", "R100", "R250", "R500", "R1000"]:
        if rstep_key not in all_results:
            continue
        for key in ["all_up", "up_with_swing_high", "up_without_swing_high"]:
            r = all_results[rstep_key].get(key, {})
            if r.get("skip") or r.get("n", 0) == 0:
                continue
            h = r["by_scheme"]["w_h2y"]
            l = r["by_scheme"]["last_2y"]
            rows.append({
                "scenario": f"{rstep_key}_{key}",
                "n": r["n"],
                "mu_signed_h2y": h["mu_signed"],
                "mu_signed_l2y": l["mu_signed"],
                "mu_rev_mfe_h2y": h["mu_rev_mfe"],
            })
    rows.sort(key=lambda x: x["mu_signed_h2y"])    # most negative (mean revert) first
    print(f"\n{'Rank':>4s} {'Scenario':35s} {'N':>5s} {'signed h2y':>12s} {'signed l2y':>12s} {'rev_mfe':>10s}")
    for i, r in enumerate(rows[:10], 1):
        flag = " ⭐" if r["mu_signed_h2y"] < -0.05 else ""
        print(f"{i:>4d} {r['scenario'][:35]:35s} {r['n']:>5d} {r['mu_signed_h2y']:>+12.4f} {r['mu_signed_l2y']:>+12.4f} {r['mu_rev_mfe_h2y']:>10.3f}{flag}")

    print("\n[G] === DOWN-CROSS bounce ranking (h2y) — most positive signed = bounce up ===")
    rows = []
    for rstep_key in ["R50", "R100", "R250", "R500", "R1000"]:
        if rstep_key not in all_results:
            continue
        for key in ["all_down", "down_with_swing_low", "down_without_swing_low"]:
            r = all_results[rstep_key].get(key, {})
            if r.get("skip") or r.get("n", 0) == 0:
                continue
            h = r["by_scheme"]["w_h2y"]
            l = r["by_scheme"]["last_2y"]
            rows.append({
                "scenario": f"{rstep_key}_{key}",
                "n": r["n"],
                "mu_signed_h2y": h["mu_signed"],
                "mu_signed_l2y": l["mu_signed"],
                "mu_rev_mfe_h2y": h["mu_rev_mfe"],
            })
    rows.sort(key=lambda x: -x["mu_signed_h2y"])
    print(f"\n{'Rank':>4s} {'Scenario':35s} {'N':>5s} {'signed h2y':>12s} {'signed l2y':>12s} {'rev_mfe':>10s}")
    for i, r in enumerate(rows[:10], 1):
        flag = " ⭐" if r["mu_signed_h2y"] > 0.05 else ""
        print(f"{i:>4d} {r['scenario'][:35]:35s} {r['n']:>5d} {r['mu_signed_h2y']:>+12.4f} {r['mu_signed_l2y']:>+12.4f} {r['mu_rev_mfe_h2y']:>10.3f}{flag}")

    return all_results


if __name__ == "__main__":
    main()
