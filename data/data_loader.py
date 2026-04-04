import yfinance as yf
import pandas as pd
from config import SYMBOLS, LOOKBACK

def load_market_data():
    data = {}

    for name, ticker in SYMBOLS.items():
        df = yf.download(ticker, period=LOOKBACK, interval="1d")
        data[name] = df["Close"]

    df = pd.DataFrame(data).dropna()
    return df
