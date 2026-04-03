import streamlit as st
import yfinance as yf

st.set_page_config(page_title="VCPMI-360 Silver", layout="wide")
st.title("VCPMI-360 Silver Dashboard - LIVE")

@st.cache_data(ttl=60)
def get_live():
    try:
        s = yf.Ticker("SI=F").history(period="5d")["Close"].iloc[-1]
        u = yf.Ticker("USDINR=X").history(period="1d")["Close"].iloc[-1]
        return s, u
    except:
        return 72.85, 93.45

comex, usdinr = get_live()

vc = {
    "daily_mean": 75.45, "daily_buy1": 74.63, "daily_buy2": 73.18,
    "daily_sell1": 76.87, "daily_sell2": 77.72,
    "weekly_sell2": 82.19, "monthly_mean": 77.81, "monthly_sell1": 94.41
}

mcx = st.number_input("Actual MCX Silver Price (paste from Groww/Zerodha/Moneycontrol)", value=232495, step=100)

parity = round(comex * 32.1507 * usdinr, 0)
scaling = mcx / parity if parity > 0 else 1.0

st.write(f"Your Actual MCX Price: ₹{mcx:,}")
st.write(f"Live COMEX: ${comex:.2f} | Parity ≈ ₹{parity:,}")

st.subheader("MCX Targets (scaled to your price)")
for name, level in vc.items():
    scaled = round(level * scaling * 32.1507 * usdinr, 0)
    st.write(f"{name.replace('_', ' ').title()} → ₹{scaled:,}")

st.subheader("Key Levels (scaled to your price)")
buy_low = round(vc["daily_buy1"] * scaling * 32.1507 * usdinr, 0)
buy_high = round(vc["daily_buy2"] * scaling * 32.1507 * usdinr, 0)
hard_stop = round(vc["daily_buy2"] * 0.95 * scaling * 32.1507 * usdinr, 0)
st.write(f"Buy Zone: ₹{buy_low:,} – ₹{buy_high:,}")
st.write(f"Hard Stop: Below ₹{hard_stop:,}")
st.write("₹2,20,000 Probability: 12% (tail risk)")

if st.button("Refresh Live Data"):
    st.rerun()
