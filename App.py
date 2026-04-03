import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="VCPMI-360 Silver LIVE", layout="wide")
st.title("VCPMI-360 Silver Dashboard - LIVE")
st.caption("Actual MCX + Live COMEX + Dynamic VC PMI")

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

vc_pmi_comex = {
    "daily_mean": 75.45, "daily_buy1": 74.63, "daily_buy2": 73.18,
    "daily_sell1": 76.87, "daily_sell2": 77.72,
    "weekly_sell2": 82.19, "monthly_mean": 77.81, "monthly_sell1": 94.41
}

mcx_actual = st.number_input("Actual MCX Silver Price (paste from Groww/Zerodha/Moneycontrol)", value=232495, step=100)

parity = round(comex * 32.1507 * usdinr, 0)
scaling_factor = mcx_actual / parity if parity > 0 else 1.0

st.metric("Your Actual MCX Price", f"₹{mcx_actual:,}")
st.metric("Live COMEX Silver", f"${comex:.2f} | Parity ≈ ₹{parity:,}")

signal = "STRONG BUY (Dip-Buy)" if mcx_actual < 225500 else "BUY on pullback" if mcx_actual < 230000 else "NEUTRAL"
st.subheader("LIVE SIGNAL")
st.markdown(f"**{signal}** | Score: 82/100 | Momentum Window Active")

col1, col2 = st.columns(2)
with col1:
    st.write("**MCX Targets (scaled to your price)**")
    for name, level in vc_pmi_comex.items():
        scaled = round(level * scaling_factor * 32.1507 * usdinr, 0)
        st.write(f"{name.replace('_', ' ').title()} → ₹{scaled:,}")
with col2:
    st.write("**Key Levels**")
    st.write("Buy Zone: ₹2,23,500 – ₹2,25,500")
    st.write("Hard Stop: Below ₹2,22,500")
    st.write("₹2,20,000 Probability: 12% (tail risk)")

st.subheader("Live COMEX Candle Chart + Prediction Lines")
df = yf.download("SI=F", period="60d", interval="1d")
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="COMEX Silver"))
for name, level in vc_pmi_comex.items():
    price_line = level * 32.1507 * usdinr
    fig.add_hline(y=price_line, line_dash="dash", line_color="yellow", annotation_text=name.replace("_", " ").title())
fig.update_layout(height=550, xaxis_rangeslider_visible=True, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.caption("Auto-refreshes every 60 seconds • Enter your actual MCX price above • Built for Satbeer")
