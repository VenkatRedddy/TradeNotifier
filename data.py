import pandas as pd
import yfinance as yf
from config import INTERVAL, PERIOD


def fetch_weekly_ohlcv(ticker):
    df = yf.download(ticker, period=PERIOD, interval=INTERVAL, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for {ticker}")
    # yfinance may return MultiIndex columns like ('Close', 'NVDA') even for
    # single tickers — flatten to simple column names ('Close', 'Open', etc.)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.dropna(inplace=True)
    return df


def fetch_batch(tickers, period="2y", interval="1wk"):
    df = yf.download(tickers, period=period, interval=interval, group_by='ticker', auto_adjust=True, threads=True, progress=False)
    return df
