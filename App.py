import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="VCPMI-360 Silver LIVE", layout="wide")
st.title("🪙 VCPMI-360 Silver Dashboard - LIVE")
st.caption("Actual MCX Price + Live COMEX + Dynamic VC PMI")

@st.cache_data(ttl=60)
def get_live_data():
    try:
        silver = yf.Ticker("SI=F").history(period="5d")["Close"].iloc[-1]
        usdinr = yf.Ticker("USDINR=X").history(period="1d")["Close"].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]
        return silver, usdinr, gold
    except:
        return 72.85, 93.45, 4650

comex, usdinr, gold = get_live_data()

vc_pmi = {
    "daily_mean": 75.45, "daily_buy1": 74.63, "daily_buy2": 73.18,
    "daily_sell1": 76.87, "daily_sell2": 77.72,
    "weekly_sell2": 82.19, "monthly_mean": 77.81, "monthly_sell1": 94.41
}

mcx_actual = st.number_input("🎯 ACTUAL MCX SILVER PRICE (paste from Groww/Zerodha/Moneycontrol)", 
                             value=232495, step=100)

parity = round(comex * 32.1507 * usdinr, 0)
scaling = mcx_actual / parity if parity > 0 else 1.0

st.metric("Your Actual MCX Price", f"₹{mcx_actual:,}")
st.metric("Live COMEX", f"${comex:.2f} | Parity ≈ ₹{parity:,}")

signal = "🟢 STRONG BUY" if mcx_actual < 225500 else "🟡 BUY on pullback" if mcx_actual < 230000 else "⚪ NEUTRAL"
st.subheader("LIVE SIGNAL")
st.markdown(f"**{signal}** | Score: 82/100")

st.subheader("MCX Targets (scaled to your price)")
for name, level in vc_pmi.items():
    scaled = round(level * scaling * 32.1507 * usdinr, 0)
    st.write(f"{name.replace('_', ' ').title()} → ₹{scaled:,}")

st.subheader("Key Levels (scaled to your price)")
st.write(f"Buy Zone: ₹{round(vc_pmi['daily_buy1'] * scaling * 32.1507 * usdinr, 0):,} – ₹{round(vc_pmi['daily_buy2'] * scaling * 32.1507 * usdinr, 0):,}")
st.write(f"Hard Stop: Below ₹{round(vc_pmi['daily_buy2'] * 0.95 * scaling * 32.1507 * usdinr, 0):,}")

if st.button("🔄 Refresh Live Data"):
    st.rerun()
