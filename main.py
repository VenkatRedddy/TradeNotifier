import os
import sys
import time
import logging

import schedule
from screener import get_most_active
from data import fetch_weekly_ohlcv
from signals import generate_signals
from chart import generate_chart
from notifier import notify

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

os.makedirs("charts", exist_ok=True)


def run_weekly_scan():
    log.info("Starting weekly scan...")
    tickers = get_most_active(count=100)
    log.info(f"Fetched {len(tickers)} most active tickers")
    alerts = []
    for ticker in tickers:
        try:
            df = fetch_weekly_ohlcv(ticker)
            df = generate_signals(df)
            last = df.iloc[-1]
            if last['BUY'] or last['SELL']:
                signal = 'BUY' if last['BUY'] else 'SELL'
                strength = last['Signal_Strength']
                chart_path = generate_chart(df, ticker)
                notify(
                    ticker=ticker,
                    signal=signal,
                    strength=strength,
                    price=last['Close'],
                    rsi=last['RSI'],
                    ema9=last['EMA9'],
                    ema21=last['EMA21'],
                    image_path=chart_path,
                )
                alerts.append(f"{strength}: {ticker}")
                log.info(f"Posted {strength} for ${ticker}")
                time.sleep(3)
        except Exception as e:
            log.error(f"Error processing {ticker}: {e}")
    log.info(f"Scan complete. {len(alerts)} alerts posted.")


def main():
    if "--once" in sys.argv:
        run_weekly_scan()
        return
    schedule.every().friday.at("16:05").do(run_weekly_scan)
    log.info("Scheduler started. Waiting for Friday 16:05...")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
