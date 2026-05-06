"""Path simulation: forward MFE/MAE within N bars from entry.

Conservative SL-first ordering (per CLAUDE.md global standard for path-sim).
All in price units (not ATR units) — caller normalizes.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def forward_mfe_mae(df: pd.DataFrame, entry_idx: np.ndarray, n_bars: int,
                    direction: str = "long") -> pd.DataFrame:
    """Compute forward MFE/MAE for each entry index over next n_bars.

    Returns DataFrame indexed by entry_idx (positions in df), columns:
      mfe_price, mae_price, ret_close (close@entry+n_bars - close@entry)
    direction: 'long' = MFE up. 'short' = MFE down.
    """
    high = df["high"].values
    low = df["low"].values
    close = df["close"].values
    n_total = len(df)

    out_mfe = np.full(len(entry_idx), np.nan)
    out_mae = np.full(len(entry_idx), np.nan)
    out_ret = np.full(len(entry_idx), np.nan)

    for i, idx in enumerate(entry_idx):
        if idx + n_bars >= n_total:
            continue
        entry_price = close[idx]
        future_high = high[idx + 1: idx + 1 + n_bars]
        future_low = low[idx + 1: idx + 1 + n_bars]
        future_close = close[idx + n_bars]
        if direction == "long":
            out_mfe[i] = future_high.max() - entry_price
            out_mae[i] = future_low.min() - entry_price  # negative number
        else:  # short
            out_mfe[i] = entry_price - future_low.min()
            out_mae[i] = entry_price - future_high.max()
        out_ret[i] = (future_close - entry_price) if direction == "long" else (entry_price - future_close)

    return pd.DataFrame({
        "mfe_price": out_mfe,
        "mae_price": out_mae,
        "ret_close": out_ret,
    }, index=entry_idx)


def hit_target_first(df: pd.DataFrame, entry_idx: np.ndarray, n_bars: int,
                     tp_price: np.ndarray, sl_price: np.ndarray,
                     direction: str = "long") -> np.ndarray:
    """For each entry, simulate bar-by-bar SL-first ordering. Return:
      +1 if TP hit, -1 if SL hit, 0 if neither within n_bars (close-out).

    tp_price/sl_price = absolute prices, len = len(entry_idx).
    """
    high = df["high"].values
    low = df["low"].values
    n_total = len(df)
    out = np.zeros(len(entry_idx), dtype=int)
    for i, idx in enumerate(entry_idx):
        if idx + n_bars >= n_total:
            continue
        tp = tp_price[i]
        sl = sl_price[i]
        for k in range(1, n_bars + 1):
            h, l = high[idx + k], low[idx + k]
            if direction == "long":
                # SL first (conservative)
                if l <= sl:
                    out[i] = -1
                    break
                if h >= tp:
                    out[i] = 1
                    break
            else:
                if h >= sl:
                    out[i] = -1
                    break
                if l <= tp:
                    out[i] = 1
                    break
    return out
