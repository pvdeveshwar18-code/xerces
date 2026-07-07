
📄 File 1: requirements.txt
On GitHub → Add file → Create new file → filename: requirements.txt → paste this → commit:

streamlit>=1.36
yfinance>=0.2.40
pandas>=2.0
numpy>=1.24
pytz>=2024.1
plotly>=5.20
statsmodels>=0.14
openpyxl>=3.1
reportlab>=4.0
nest_asyncio>=1.6
emergentintegrations
--extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
📄 File 2: .streamlit/config.toml
On GitHub → Add file → Create new file → filename: .streamlit/config.toml (the slash creates the folder) → paste this → commit:

[theme]
base = "dark"
primaryColor = "#00c8ff"
backgroundColor = "#020813"
secondaryBackgroundColor = "#0a192f"
textColor = "#e2e8f0"
font = "monospace"

[server]
headless = true
enableCORS = false

[browser]
gatherUsageStats = false
📄 File 3: README.md
On GitHub → Add file → Create new file → filename: README.md → paste this → commit:

# XERCES // Quant Engine

A next-generation Streamlit dashboard for Indian equity (NSE/BSE) analysis — 600+ stocks across 18 sectors, complete with technical indicators, AI analyst, forecasting, backtesting, and portfolio optimization.

## Features

### Core Analytics (11 tabs)
- **Chart** — Candlesticks, SMA 20/50/200, Bollinger Bands, RSI, MACD, Stochastic, Volume
- **Forecast** — ARIMA (5x5 AIC grid search) + Holt-Winters consensus with 60-day MAPE + directional accuracy
- **Backtest** — 4 strategies (SMA/RSI/BB/MACD) on 5-year data, next-day open execution
- **Scanner** — Bulk multi-sector scanner with BUY/SELL/HOLD signals + position sizing
- **Risk Calculator** — Position-sizing based on ATR and R:R
- **Portfolio** — MPT optimizer (3000 Monte Carlo simulations) + custom portfolio tracker with rotation advisor
- **FII/DII Flows** — Live NSE institutional flow data
- **Options Chain** — Full option chain, PCR, Max Pain analysis
- **Fundamentals** — P/E, P/B, ROE, ROCE, Debt/Equity, EPS from Screener.in
- **News & Sentiment** — Google News / Yahoo RSS with keyword-based sentiment scoring
- **Manual** — Complete reference guide

### XERCES+ Enhancements (5 new tabs)
- **Heatmap** — Live 1-day sector performance + 5-min intraday candles
- **Compare** — Side-by-side 2–4 stocks with correlation matrix + risk/return stats
- **AI Analyst** — Multi-turn chatbot powered by Claude Sonnet 4.6 / GPT-5.4 / Gemini. One-click trade thesis & news summarization
- **Journal** — Persistent trade log with P&L tracking, win-rate, equity curve
- **Export** — PDF stock reports (with optional AI thesis) + multi-sheet Excel workbook

### Sidebar
- **Watchlist** — Persistent, add/remove any stock
- **Alerts** — Price / RSI threshold alerts, auto-triggered on refresh

## Run Locally

```bash
git clone https://github.com/pvdeveshwar18-code/code/arima.git
cd arima
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501.

## Deploy to Streamlit Community Cloud

1. Push all files to your repo
2. Go to share.streamlit.io -> deploy your app
3. In app settings, add a secret:
   ```
   EMERGENT_LLM_KEY = "sk-emergent-2191f894997De47509"
   ```
4. Deploy — you get a permanent URL

## Disclaimer

XERCES is a research and analysis tool. Not SEBI registered. Not financial advice. Data from Y
