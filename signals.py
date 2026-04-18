import pandas as pd
from config import EMA_FAST, EMA_SLOW, RSI_PERIOD, RSI_OVERSOLD, RSI_OVERBOUGHT


def add_ema_signals(df):
    df['EMA9']  = df['Close'].ewm(span=EMA_FAST, adjust=False).mean()
    df['EMA21'] = df['Close'].ewm(span=EMA_SLOW, adjust=False).mean()
    df['EMA_Spread'] = df['EMA9'] - df['EMA21']
    df['EMA_Bull_Cross'] = (df['EMA9'] > df['EMA21']) & (df['EMA9'].shift(1) <= df['EMA21'].shift(1))
    df['EMA_Bear_Cross'] = (df['EMA9'] < df['EMA21']) & (df['EMA9'].shift(1) >= df['EMA21'].shift(1))
    df['EMA_Curl_Up'] = (df['EMA_Spread'] > df['EMA_Spread'].shift(1)) & (df['EMA9'] < df['EMA21'])
    return df


def add_macd_signals(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD']        = ema12 - ema26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist']   = df['MACD'] - df['MACD_Signal']
    df['MACD_Curl_Up']   = (df['MACD_Hist'] > df['MACD_Hist'].shift(1)) & (df['MACD_Hist'].shift(1) < 0)
    df['MACD_Curl_Down'] = (df['MACD_Hist'] < df['MACD_Hist'].shift(1)) & (df['MACD_Hist'].shift(1) > 0)
    return df


def add_rsi(df):
    delta = df['Close'].diff()
    gain  = delta.where(delta > 0, 0).rolling(RSI_PERIOD).mean()
    loss  = (-delta.where(delta < 0, 0)).rolling(RSI_PERIOD).mean()
    rs    = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['RSI_Oversold']   = df['RSI'] < RSI_OVERSOLD
    df['RSI_Overbought'] = df['RSI'] > RSI_OVERBOUGHT
    return df


def generate_signals(df):
    df = add_ema_signals(df)
    df = add_macd_signals(df)
    df = add_rsi(df)
    bullish_trigger = df['EMA_Bull_Cross'] | df['EMA_Curl_Up'] | df['MACD_Curl_Up']
    df['BUY'] = bullish_trigger & ~df['RSI_Overbought']
    bearish_trigger = df['EMA_Bear_Cross'] | df['MACD_Curl_Down']
    df['SELL'] = bearish_trigger & ~df['RSI_Oversold']
    df['Signal_Strength'] = 'NONE'
    df.loc[df['BUY']  & df['RSI_Oversold'],    'Signal_Strength'] = 'STRONG_BUY'
    df.loc[df['BUY']  & ~df['RSI_Oversold'],   'Signal_Strength'] = 'BUY'
    df.loc[df['SELL'] & df['RSI_Overbought'],   'Signal_Strength'] = 'STRONG_SELL'
    df.loc[df['SELL'] & ~df['RSI_Overbought'],  'Signal_Strength'] = 'SELL'
    return df
