# 📈 Nifty50 Supertrend Scanner

A web app that scans all **Nifty 50 stocks** for **Supertrend (15,3.5)** signals on **1h timeframe**.

### Features
- JSON output of Buy/Sell signals (`/scan`)
- Candlestick + Supertrend chart (`/chart?symbol=RELIANCE.NS`)
- Flask + yFinance + mplfinance

### Run Locally
```bash
pip install -r requirements.txt
python app.py
```
Visit: `http://127.0.0.1:5000`
