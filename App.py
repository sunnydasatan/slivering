import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="VCPMI-360 Silver LIVE", layout="wide")
st.title("🪙 VCPMI-360 Silver Dashboard - LIVE")
st.caption("Actual MCX + Live COMEX • Dynamically Scaled VC PMI + Gann + Fib")

# Live data with robust error handling and longer cache
@st.cache_data(ttl=60)  # 60 seconds to avoid rate limits
def get_live_data():
    try:
        silver = yf.Ticker("SI=F").history(period="5d")["Close"].iloc[-1]
        usdinr = yf.Ticker("USDINR=X").history(period="1d")["Close"].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]
        oil = yf.Ticker("CL=F").history(period="1d")["Close"].iloc[-1]
        return silver, usdinr, gold, oil
    except:
        # Fallback values if rate limit hit
        return 72.85, 93.45, 4650, 111

comex, usdinr, gold, oil = get_live_data()

vc_pmi_comex = {
    "daily_mean": 75.45, "daily_buy1": 74.63, "daily_buy2": 73.18,
    "daily_sell1": 76.87, "daily_sell2": 77.72,
    "weekly_sell2": 82.
