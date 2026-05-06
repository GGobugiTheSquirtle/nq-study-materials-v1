"""Common indicators: EMA / ATR / SMA / Bollinger.

NQ 5m bar input. All numpy/pandas based, vectorized."""
from __future__ import annotations
import numpy as np
import pandas as pd


def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False).mean()


def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(window=length, min_periods=length).mean()


def atr(df: pd.DataFrame, length: int = 14) -> pd.Series:
    """Wilder's ATR."""
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    # Wilder smoothing = EMA with alpha=1/length
    return tr.ewm(alpha=1.0 / length, adjust=False).mean()


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add common indicators to a copy of df."""
    out = df.copy()
    out["ema20"] = ema(out["close"], 20)
    out["ema50"] = ema(out["close"], 50)
    out["ema200"] = ema(out["close"], 200)
    out["atr14"] = atr(out, 14)
    return out


def regime_label(df: pd.DataFrame, slope_window: int = 200) -> pd.Series:
    """Simple regime: BULL (ema200 slope > +0.05% per bar avg, close > ema200)
    BEAR (slope < -0.05%, close < ema200)
    CHOP (else).
    """
    ema200 = df["ema200"]
    slope = ema200.pct_change(slope_window)  # change over slope_window bars
    bull_thresh = 0.005   # 0.5% over 200 bars
    bear_thresh = -0.005
    above = df["close"] > ema200
    label = pd.Series(index=df.index, dtype="object")
    label[(slope > bull_thresh) & above] = "BULL"
    label[(slope < bear_thresh) & ~above] = "BEAR"
    label = label.fillna("CHOP")
    return label
