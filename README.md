# 📈 TradeNotifier — Weekly EMA9/21 Trader Notifier

A fully automated Python application that scans the **top 100 most active tickers by volume** from Yahoo Finance, detects **weekly EMA9/EMA21 crossover signals** with **MACD curl confirmation** and **RSI filtering**, generates annotated charts, and posts alerts to **Twitter/X**.

---

## ✨ Features

- 📊 **Weekly EMA9/21 Crossover** — detects bullish and bearish crossovers on the weekly timeframe
- 📉 **MACD Curl Detection** — confirms momentum with histogram curl (below zero curling up / above zero curling down)
- 🔍 **RSI Filter** — avoids overbought entries (RSI > 75) and oversold exits (RSI < 30); flags STRONG signals when RSI confirms
- 🖼️ **Auto Chart Generation** — 4-panel annotated charts: candlestick + EMA overlays, volume, RSI(14), MACD histogram
- 🐦 **Twitter/X Alerts** — automatically uploads charts and posts signal tweets with emoji and hashtags
- ⚙️ **GitHub Actions Deployment** — runs every Friday at 16:05 ET via scheduled cron workflow

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/VenkatRedddy/TradeNotifier.git
cd TradeNotifier

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env and fill in your Twitter/X API credentials

# 4. Run a one-shot scan
python main.py --once
```

---

## ⚙️ Configuration

Edit `config.py` or set values via environment variables.

| Constant | Default | Description |
|---|---|---|
| `EMA_FAST` | `9` | Fast EMA period |
| `EMA_SLOW` | `21` | Slow EMA period |
| `RSI_PERIOD` | `14` | RSI lookback period |
| `RSI_OVERSOLD` | `30` | RSI level considered oversold |
| `RSI_OVERBOUGHT` | `75` | RSI level considered overbought |
| `INTERVAL` | `"1wk"` | Candle timeframe (weekly) |
| `PERIOD` | `"2y"` | History to download (2 years) |
| `CHART_LOOKBACK` | `52` | Number of weekly candles shown in chart |
| `MOST_ACTIVE_COUNT` | `100` | Number of tickers to screen |

---

## 📐 Signal Logic

### Decision Matrix

| EMA Cross | MACD Curl | RSI | Signal |
|---|---|---|---|
| 🟢 Bullish crossover | — | < 75 | **BUY** ✅ |
| — | 🟢 Curl Up (below zero) | < 75 | **BUY** ✅ |
| 🟢 Bullish curl (spread widening) | — | < 75 | **BUY** ✅ |
| Any bullish | — | < 30 (oversold) | **STRONG BUY** 🔥🟢 |
| Any bullish | — | > 75 (overbought) | ⚠️ Skipped |
| 🔴 Bearish crossover | — | > 30 | **SELL** 🔴 |
| — | 🔴 Curl Down (above zero) | > 30 | **SELL** 🔴 |
| Any bearish | — | > 75 (overbought) | **STRONG SELL** 🔥🔴 |
| Any bearish | — | < 30 (oversold) | ⚠️ Skipped |

---

## 📊 Chart Layout

Each generated chart has **4 panels**:

1. **Candlestick** — Weekly OHLCV candles with EMA9 (blue) and EMA21 (orange) overlays, plus ▲ BUY / ▼ SELL markers
2. **Volume** — Weekly volume bars
3. **RSI(14)** — Relative Strength Index with dashed lines at 30 (oversold) and 75 (overbought)
4. **MACD Histogram** — Difference between MACD line and signal line; curl direction drives confirmation signals

---

## 🚢 Deployment

### GitHub Actions (Recommended — Free)

The included workflow (`.github/workflows/weekly_scan.yml`) runs automatically every **Friday at 20:05 UTC (16:05 EDT / 15:05 EST — exact local time varies by daylight saving)**. You can also trigger it manually via `workflow_dispatch`.

**Setup:**
1. Go to **Settings → Secrets and variables → Actions** in your repository
2. Add the following repository secrets:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_SECRET`

### VPS / Always-On Server

```bash
# Run the built-in scheduler (fires every Friday at 16:05)
python main.py

# Or use cron
5 20 * * 5 cd /path/to/TradeNotifier && python main.py --once
```

---

## 🔑 Twitter/X API Requirements

You need a **Twitter/X Developer account** with at least **Basic** access to:
- Upload media (v1.1 endpoint)
- Post tweets (v2 endpoint)

Free tier allows ~1,500 tweets/month which is more than sufficient for weekly scans.

---

## 📁 Project Structure

```
TradeNotifier/
├── config.py                          # API keys, thresholds, constants
├── screener.py                        # Fetch top 100 most active tickers
├── data.py                            # Download weekly OHLCV via yfinance
├── signals.py                         # EMA9/21, MACD curl, RSI logic
├── chart.py                           # Annotated chart generation
├── notifier.py                        # Twitter/X image upload & tweet
├── main.py                            # Orchestrator + scheduler
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variable template
├── .gitignore
└── .github/workflows/weekly_scan.yml  # GitHub Actions cron workflow
```

---

## 📄 License

This project is provided as-is for educational and informational purposes. Not financial advice.
