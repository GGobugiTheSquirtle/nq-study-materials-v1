"""Time-decay exponential weighting.

w(t) = exp(-lambda * (T - t)), lambda = ln(2) / half_life

Reports 5 schemes for robustness:
- w_eq      : equal weight (no decay)
- w_h2y     : half-life 2 years (PRIMARY for judgment)
- w_h1y     : half-life 1 year (recency-biased)
- last_2y   : hard cutoff last 2 years
- last_1y   : hard cutoff last 1 year (overfitting risk)
"""
from __future__ import annotations
import numpy as np
import pandas as pd

YEAR_DAYS = 365.25


def exp_weights(times: pd.DatetimeIndex, half_life_years: float) -> np.ndarray:
    """Return weights normalized to sum=N (effective sample size matches mean weighting).

    Most recent point => weight ~1.0.
    """
    T = times.max()
    age_days = np.asarray((T - times).total_seconds()) / 86400.0
    lam = np.log(2) / (half_life_years * YEAR_DAYS)
    w = np.exp(-lam * age_days)
    # Normalize so sum(w) = N → mean of weighted = mean of unweighted reference
    w = w * (len(w) / w.sum())
    return np.asarray(w)


def get_all_weights(times: pd.DatetimeIndex) -> dict[str, np.ndarray]:
    """Get all 5 weighting schemes.

    Returns dict: scheme_name -> weights array (len = len(times)).
    """
    T = times.max()
    cutoff_2y = T - pd.Timedelta(days=2 * YEAR_DAYS)
    cutoff_1y = T - pd.Timedelta(days=1 * YEAR_DAYS)

    n = len(times)
    w_eq = np.ones(n)
    w_h2y = exp_weights(times, half_life_years=2.0)
    w_h1y = exp_weights(times, half_life_years=1.0)

    last_2y = np.where(times >= cutoff_2y, 1.0, 0.0)
    if last_2y.sum() > 0:
        last_2y = last_2y * (n / last_2y.sum())
    last_1y = np.where(times >= cutoff_1y, 1.0, 0.0)
    if last_1y.sum() > 0:
        last_1y = last_1y * (n / last_1y.sum())

    return {
        "w_eq": w_eq,
        "w_h2y": w_h2y,
        "w_h1y": w_h1y,
        "last_2y": last_2y,
        "last_1y": last_1y,
    }


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.average(values, weights=weights))


def weighted_std(values: np.ndarray, weights: np.ndarray) -> float:
    """Weighted standard deviation (population)."""
    mu = weighted_mean(values, weights)
    var = np.average((values - mu) ** 2, weights=weights)
    return float(np.sqrt(var))


def effective_n(weights: np.ndarray) -> float:
    """Kish effective sample size: N_eff = (sum w)^2 / sum w^2."""
    s = weights.sum()
    return float(s * s / np.sum(weights ** 2))


if __name__ == "__main__":
    times = pd.date_range("2016-01-01", "2026-04-01", freq="D")
    weights = get_all_weights(times)
    for name, w in weights.items():
        print(f"{name:10s}: sum={w.sum():,.0f}, N_eff={effective_n(w):,.0f}, w[0]={w[0]:.4f}, w[-1]={w[-1]:.4f}")
