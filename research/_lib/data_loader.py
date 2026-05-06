"""NQ 5m data loader.

Source: backtest_data/nq_10y/nq-5m_bk.csv (FirstRateData format)
Format: DD/MM/YYYY;HH:MM;O;H;L;C;V (semicolon delimited, UK date order)
Period: 2008-11 ~ 2026-04 (~17.5y, ~1.2M bars)
"""
from __future__ import annotations
import pandas as pd
from pathlib import Path

DATA_5M = Path(r"c:/Users/minb0/Desktop/Main folder/투자공부/backtest_data/nq_10y/nq-5m_bk.csv")
DATA_15M = Path(r"c:/Users/minb0/Desktop/Main folder/투자공부/backtest_data/nq_10y/nq-15m_bk.csv")
DATA_1M = Path(r"c:/Users/minb0/Desktop/Main folder/투자공부/backtest_data/nq_10y/nq-1m_bk.csv")


def load_nq(tf: str = "5m", start: str | None = "2016-01-01", end: str | None = None) -> pd.DataFrame:
    """Load NQ OHLCV at given timeframe.

    Returns DataFrame with UTC-naive index (data is exchange time, no TZ),
    columns: open, high, low, close, volume.
    Index name: 'datetime'.
    """
    path = {"5m": DATA_5M, "15m": DATA_15M, "1m": DATA_1M}[tf]
    df = pd.read_csv(
        path,
        sep=";",
        header=None,
        names=["date", "time", "open", "high", "low", "close", "volume"],
        dtype={"date": str, "time": str},
    )
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format="%d/%m/%Y %H:%M")
    df = df.drop(columns=["date", "time"]).set_index("datetime").sort_index()
    if start:
        df = df.loc[start:]
    if end:
        df = df.loc[:end]
    return df


if __name__ == "__main__":
    df = load_nq("5m", start="2016-01-01")
    print(f"Loaded {len(df):,} bars")
    print(f"Range: {df.index[0]} ~ {df.index[-1]}")
    print(df.head(3))
    print(df.tail(3))
