# XERCES+ Quant Engine — PRD

## Original Problem Statement
User provided a comprehensive Streamlit-based Indian equity quant engine (`app.py`, 2268 lines) covering NSE/BSE with 600+ stocks, technical analysis, ARIMA + Holt-Winters forecasting, backtesting, market scanner, portfolio optimizer, FII/DII flows, options chain, fundamentals, and news/sentiment. User asked: **"build a website around this OR add to the existing Streamlit code."** Chose option (a) — extend the existing Streamlit app. Requested all 5 improvement categories (Polish, New Analytics, AI, Data/Export, UI) without removing any existing feature.

## Architecture
- **Runtime**: Streamlit (Python) on port 8501
- **Data sources**: Yahoo Finance (yfinance), NSE India (FII/DII, options), Google News RSS, Screener.in (fundamentals)
- **AI**: `emergentintegrations` library → Claude Sonnet 4.6 via Emergent LLM Key (multi-model support: GPT-5.4, Gemini 3 Flash, Claude Haiku 4.5)
- **Persistence**: JSON + CSV files in `/app/streamlit_app/data/`
- **Files**:
  - `/app/streamlit_app/app.py` — main app (2700+ lines; original preserved + new tabs appended)
  - `/app/streamlit_app/app_original.py` — untouched backup of user's original
  - `/app/streamlit_app/xerces_plus.py` — new enhancement module (watchlist, alerts, AI, heatmap, compare, journal, PDF/Excel export)
  - `/app/streamlit_app/data/` — persistent state (watchlist.json, alerts.json, journal.csv)

## Users
- Retail traders / long-term investors in Indian equities (NSE/BSE)
- Quant hobbyists running technicals + forecasts locally
- Portfolio holders tracking custom baskets and doing rotation analysis

## Core Requirements (Static)
- Preserve ALL 11 original tabs and every existing feature untouched
- Add polish, new analytics, AI, exports, and UX improvements as additive enhancements
- No paid keys required (Emergent LLM Key auto-provisioned)

## What's Been Implemented — 2026-01 (Session 1)
### Preserved (original 11 tabs)
📊 CHART · 🔮 FORECAST · 📈 BACKTEST · 📡 SCANNER · 🛡️ RISK · 💼 PORTFOLIO · 📊 FII/DII · 🎯 OPTIONS · 📋 FUNDAMENTALS · 📰 NEWS · ❓ MANUAL

### NEW — 5 tabs
1. **🔥 HEATMAP** — Live 1-day sector performance across all 18 sectors (batch download), plus 5-min intraday candlestick chart for the selected stock. Market-breadth KPI (% bullish sectors).
2. **🔄 COMPARE** — Pick 2–4 stocks, get normalized price chart (base=100), correlation matrix heatmap, and risk/return stats table (Return, Vol, Sharpe, MaxDD).
3. **🤖 AI ANALYST** — Multi-turn chatbot for the selected stock. Auto-injects live context (price, RSI, MACD, SMAs, ATR, fundamentals, latest 10 news headlines). One-click Trade Thesis generator + News Summarization. Model selector: Claude Sonnet 4.6 (default), GPT-5.4, Gemini 3 Flash, Claude Haiku 4.5.
4. **📓 JOURNAL** — Trade log with entry/exit, side, strategy, notes; auto-computed P&L (₹ + %). Win-rate, total P&L KPIs and cumulative equity curve. Persistent CSV, editable table.
5. **📄 EXPORT** — One-click **PDF report** (with optional AI-generated thesis + news summary) via reportlab, and multi-sheet **Excel workbook** via openpyxl (OHLCV+indicators, backtest trades, scanner results, journal, watchlist).

### NEW — sidebar
- **⭐ WATCHLIST** — Persistent (JSON on disk). Add/remove selected stock, jump between watched stocks
- **🚨 ALERTS** — Persistent price/RSI threshold alerts with `>`/`<` conditions. Evaluated on every page load; triggered alerts show as top banner + tagged as "🔔 FIRED".

### Fixes / Polish
- Preserved CSS theme (Orbitron + Space Mono cyber-terminal aesthetic)
- Added the new features with matching visual language (glass cards, colour-coded signals)
- Updated MANUAL tab with new feature docs

### Verified Working (2026-01)
- ✅ Streamlit boots on :8501, landing page renders NIFTY/BANK NIFTY/SENSEX/INDIA VIX live
- ✅ Full 16-tab layout renders on RELIANCE analysis view
- ✅ AI Analyst → Claude Sonnet 4.6 returns valid contextual response
- ✅ PDF export → 3KB valid PDF
- ✅ Excel export → 5KB valid XLSX
- ✅ Watchlist / Alerts / Journal all persist to disk

## Prioritized Backlog
### P1 (near-term polish)
- Stream AI responses token-by-token (currently non-streaming to keep Streamlit simple)
- Persist AI chat history across Streamlit reruns (currently session-only)
- Add sortable/filterable master watchlist view as a dedicated section

### P2 (nice-to-have)
- Email/Telegram delivery of triggered alerts (needs SendGrid/Telegram bot)
- Live intraday auto-refresh via `st.autorefresh` (currently manual)
- Multi-user auth (currently single-user machine-local)
- Add Nifty 50 / Bank Nifty options chain (currently equity F&O only)

### P3 (future)
- Voice-input to AI Analyst (STT via Whisper)
- WhatsApp share of PDF report
- LSTM / transformer forecast alongside ARIMA
- Coin-based paper trading with leaderboard
