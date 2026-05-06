"""Effect size + bootstrap CI under weighting.

User policy (2026-05-06): "너무 보수적으로 가지 않아도 경향성으로 의미 충분".
→ Focus on effect size + direction across weighting schemes.
→ p-value 부수적 (alpha=0.05 reference, no Bonferroni).
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from .weighting import weighted_mean, weighted_std, effective_n


def cohen_d(group_a: np.ndarray, group_b: np.ndarray,
            w_a: np.ndarray | None = None, w_b: np.ndarray | None = None) -> float:
    """Cohen's d. group_a - group_b in pooled-std units. Supports weights."""
    if w_a is None:
        w_a = np.ones(len(group_a))
    if w_b is None:
        w_b = np.ones(len(group_b))
    mu_a = weighted_mean(group_a, w_a)
    mu_b = weighted_mean(group_b, w_b)
    sd_a = weighted_std(group_a, w_a)
    sd_b = weighted_std(group_b, w_b)
    n_a, n_b = effective_n(w_a), effective_n(w_b)
    pooled = np.sqrt(((n_a - 1) * sd_a**2 + (n_b - 1) * sd_b**2) / max(n_a + n_b - 2, 1))
    if pooled == 0:
        return 0.0
    return (mu_a - mu_b) / pooled


def bootstrap_ci(values: np.ndarray, weights: np.ndarray,
                 stat_fn=weighted_mean, n_boot: int = 1000, ci: float = 0.95,
                 rng_seed: int = 42) -> tuple[float, float]:
    """Weighted bootstrap CI. Sampling with replacement using normalized weights as p."""
    rng = np.random.default_rng(rng_seed)
    n = len(values)
    p = weights / weights.sum()
    boot_stats = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.choice(n, size=n, replace=True, p=p)
        # Resampled weights = uniform (we already encoded weight via sampling probability)
        boot_stats[i] = stat_fn(values[idx], np.ones(n))
    alpha = (1 - ci) / 2
    return float(np.quantile(boot_stats, alpha)), float(np.quantile(boot_stats, 1 - alpha))


def hit_rate(values: np.ndarray, weights: np.ndarray, threshold: float, direction: str = ">=") -> float:
    """Weighted hit rate: % of values that meet threshold."""
    if direction == ">=":
        hits = (values >= threshold).astype(float)
    elif direction == "<=":
        hits = (values <= threshold).astype(float)
    else:
        raise ValueError(direction)
    return weighted_mean(hits, weights)


def interpret_d(d: float) -> str:
    abs_d = abs(d)
    if abs_d < 0.10:
        return "negligible"
    if abs_d < 0.30:
        return "small"
    if abs_d < 0.50:
        return "medium"
    if abs_d < 0.80:
        return "large"
    return "very large"


def judge_phase_a(d_by_scheme: dict[str, float], threshold: float = 0.15) -> str:
    """Phase A judge rule (per master plan).

    GO     = w_h2y >= threshold AND all schemes positive (>= 0)
    PARTIAL= w_h2y >= threshold but some scheme < 0 OR < threshold/2
    DECAY  = w_eq > w_h2y > last_2y (monotonic decay)
    NOGO   = w_h2y < threshold AND last_2y < threshold
    """
    eq = d_by_scheme.get("w_eq", 0)
    h2y = d_by_scheme.get("w_h2y", 0)
    h1y = d_by_scheme.get("w_h1y", 0)
    l2y = d_by_scheme.get("last_2y", 0)
    l1y = d_by_scheme.get("last_1y", 0)

    # DECAY check (all positive but decreasing recency = stride/old artifact)
    if eq > h2y > l2y > 0 and (eq - l2y) > 0.10:
        return "DECAY"

    # NOGO: both primary and short-window fail
    if h2y < threshold and l2y < threshold:
        return "NOGO"

    # GO: primary passes AND no scheme negative
    all_positive = all(v >= 0 for v in [eq, h2y, h1y, l2y, l1y])
    if h2y >= threshold and all_positive:
        return "GO"

    # PARTIAL: somewhere in between
    return "PARTIAL"


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    a = rng.normal(0.5, 1, 1000)
    b = rng.normal(0.0, 1, 1000)
    print(f"Cohen d = {cohen_d(a, b):.3f}, interpretation = {interpret_d(cohen_d(a, b))}")
