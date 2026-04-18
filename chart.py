import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
import os
from config import RSI_OVERSOLD, RSI_OVERBOUGHT, CHART_LOOKBACK


def generate_chart(df, ticker, save_path=None):
    if save_path is None:
        os.makedirs("charts", exist_ok=True)
        save_path = f"charts/{ticker}_weekly.png"

    plot_df = df.tail(CHART_LOOKBACK).copy()
    buy_markers  = plot_df['Close'].where(plot_df['BUY'], None)
    sell_markers = plot_df['Close'].where(plot_df['SELL'], None)
    rsi_30 = pd.Series(RSI_OVERSOLD, index=plot_df.index)
    rsi_75 = pd.Series(RSI_OVERBOUGHT, index=plot_df.index)

    add_plots = [
        mpf.make_addplot(plot_df['EMA9'], color='#2196F3', width=1.5),
        mpf.make_addplot(plot_df['EMA21'], color='#FF9800', width=1.5),
        mpf.make_addplot(buy_markers, type='scatter', marker='^', color='#00E676', markersize=120),
        mpf.make_addplot(sell_markers, type='scatter', marker='v', color='#FF1744', markersize=120),
        mpf.make_addplot(plot_df['RSI'], panel=2, color='purple', ylabel='RSI(14)', width=1.2),
        mpf.make_addplot(rsi_30, panel=2, color='green', linestyle='--', width=0.7),
        mpf.make_addplot(rsi_75, panel=2, color='red', linestyle='--', width=0.7),
        mpf.make_addplot(plot_df['MACD_Hist'], panel=3, type='bar', color='dimgray', ylabel='MACD Hist'),
    ]

    mc = mpf.make_marketcolors(up='#00E676', down='#FF1744', edge='inherit', wick='inherit', volume='in')
    style = mpf.make_mpf_style(marketcolors=mc, gridstyle=':', rc={'font.size': 9})

    fig, axes = mpf.plot(
        plot_df, type='candle', addplot=add_plots,
        title=f'\n${ticker} Weekly — EMA9/21 + RSI + MACD',
        volume=True, style=style, figsize=(14, 10),
        panel_ratios=(4, 1, 1.5, 1.5), returnfig=True
    )

    fig.text(0.5, 0.01, 'Weekly EMA9/21 Scanner', ha='center', fontsize=8, color='gray', alpha=0.6)
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return save_path
