from flask import Flask, render_template, jsonify, request
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import os

app = Flask(__name__)

# --- Supertrend Function ---
def supertrend(df, period=15, multiplier=3.5):
    df['ATR'] = df['High'].rolling(period).max() - df['Low'].rolling(period).min()
    df['ATR'] = df['ATR'].ewm(span=period, adjust=False).mean()

    hl2 = (df['High'] + df['Low']) / 2
    df['UpperBand'] = hl2 + (multiplier * df['ATR'])
    df['LowerBand'] = hl2 - (multiplier * df['ATR'])

    df['Supertrend'] = df['UpperBand']
    direction = True

    for i in range(1, len(df)):
        if df['Close'][i] > df['Supertrend'][i-1]:
            direction = True
        elif df['Close'][i] < df['Supertrend'][i-1]:
            direction = False

        if direction:
            df['Supertrend'][i] = df['LowerBand'][i]
        else:
            df['Supertrend'][i] = df['UpperBand'][i]

    return df

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan')
def scan():
    nifty50 = [
        "RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","ICICIBANK.NS",
        "HINDUNILVR.NS","SBIN.NS","BAJFINANCE.NS","ITC.NS","KOTAKBANK.NS"
    ]  # shortened for demo

    results = {}
    for symbol in nifty50:
        try:
            df = yf.download(symbol, period="15d", interval="1h")
            df = supertrend(df)
            if df['Close'].iloc[-1] > df['Supertrend'].iloc[-1]:
                results[symbol] = "Buy"
            elif df['Close'].iloc[-1] < df['Supertrend'].iloc[-1]:
                results[symbol] = "Sell"
            else:
                results[symbol] = "No Signal"
        except Exception as e:
            results[symbol] = f"Error: {e}"
    return jsonify(results)

@app.route('/chart')
def chart():
    symbol = request.args.get("symbol", "RELIANCE.NS")
    df = yf.download(symbol, period="3mo", interval="1h")
    df = supertrend(df)

    # Plot candlestick + Supertrend
    ap = mpf.make_addplot(df['Supertrend'], color='red')
    chart_path = f"static/{symbol}_chart.png"
    mpf.plot(df, type="candle", style="yahoo", addplot=ap, savefig=chart_path)

    return f"<h2>{symbol} - Supertrend Chart</h2><img src='/{chart_path}' width='100%'>"

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
