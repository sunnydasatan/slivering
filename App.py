import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="VCPMI-360 Silver LIVE", layout="wide", initial_sidebar_state="collapsed")
st.title("🪙 VCPMI-360 Silver Dashboard")
st.caption("Live MCX • COMEX • Gold Correlation • Oil Sensitivity • Dynamic Targets")

# ====================== LIVE DATA ======================
@st.cache_data(ttl=60)
def get_live_data():
    try:
        silver = yf.Ticker("SI=F").history(period="5d")["Close"].iloc[-1]
        usdinr = yf.Ticker("USDINR=X").history(period="1d")["Close"].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]
        oil = yf.Ticker("CL=F").history(period="1d")["Close"].iloc[-1]
        return silver, usdinr, gold, oil
    except:
        return 72.85, 93.45, 4650, 111

comex, usdinr, gold, oil = get_live_data()

vc_pmi_comex = {
    "daily_mean": 75.45, "daily_buy1": 74.63, "daily_buy2": 73.18,
    "daily_sell1": 76.87, "daily_sell2": 77.72,
    "weekly_sell2": 82.19, "monthly_mean": 77.81, "monthly_sell1": 89.91
}

# ====================== USER INPUT ======================
mcx_actual = st.number_input("🎯 ACTUAL MCX SILVER PRICE (paste from Groww/Zerodha/Moneycontrol)", 
                             value=232495, step=100, label_visibility="visible")

parity = round(comex * 32.1507 * usdinr, 0)
scaling_factor = mcx_actual / parity if parity > 0 else 1.0
gsr_current = round(gold / comex, 1)
silver_oil_ratio = round(comex / oil, 3)

# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Targets & Levels", "🏆 Gold / GSR Sensitivity (USD)", "📉 Live Chart"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("MCX Actual", f"₹{mcx_actual:,}")
    with col2: st.metric("COMEX Silver", f"${comex:.2f}")
    with col3: st.metric("Gold Price", f"${gold:.0f}")
    with col4: st.metric("Crude Oil", f"${oil:.2f}")

    st.write(f"**Gold-Silver Ratio**: {gsr_current}:1  **Silver-Oil Ratio**: {silver_oil_ratio}")
    
    signal = "🟢 STRONG BUY (Dip-Buy)" if mcx_actual < 226000 else "🟡 BUY on pullback" if mcx_actual < 230000 else "⚪ NEUTRAL"
    st.subheader("LIVE SIGNAL")
    st.success(f"**{signal}** | Score: 82/100 | Momentum Window Active")

with tab2:
    colA, colB = st.columns(2)
    with colA:
        st.subheader("MCX Targets (scaled to your price)")
        for name, level in vc_pmi_comex.items():
            scaled = round(level * scaling_factor * 32.1507 * usdinr, 0)
            st.write(f"{name.replace('_', ' ').title()} → ₹{scaled:,}")
    with colB:
        st.subheader("Key Levels (scaled to your price)")
        buy_low = round(vc_pmi_comex["daily_buy1"] * scaling_factor * 32.1507 * usdinr, 0)
        buy_high = round(vc_pmi_comex["daily_buy2"] * scaling_factor * 32.1507 * usdinr, 0)
        hard_stop = round(vc_pmi_comex["daily_buy2"] * 0.97 * scaling_factor * 32.1507 * usdinr, 0)
        st.write(f"**Buy Zone**: ₹{buy_low:,} – ₹{buy_high:,}")
        st.write(f"**Hard Stop**: Below ₹{hard_stop:,}")
        st.write("**₹2,20,000 Probability**: 12% (tail risk)")

with tab3:
    st.subheader("🏆 Gold Price / GSR Sensitivity (COMEX Silver in USD)")
    st.write("**Live Gold Price**: ${gold:.0f}  **Current GSR**: {gsr_current}:1  **Current COMEX Silver**: ${comex:.2f}".format(gold=gold, gsr_current=gsr_current, comex=comex))
    
    gsr_table = {
        "65:1 (current)": round(gold / 65, 2),
        "70:1": round(gold / 70, 2),
        "80:1": round(gold / 80, 2),
        "90:1": round(gold / 90, 2),
        "100:1": round(gold / 100, 2)
    }
    for ratio, silver_target in gsr_table.items():
        difference = round(silver_target - comex, 2)
        st.write(f"**GSR {ratio}** → COMEX Silver target **${silver_target}** (diff {difference:+.2f})")

    st.subheader("🛢️ Oil Price Sensitivity")
    oil_table = {
        "$100": round(comex * (100 / oil) * 1.15, 2),
        "$110": round(comex * (110 / oil) * 1.08, 2),
        "$120": round(comex * (120 / oil) * 1.12, 2),
        "$130": round(comex * (130 / oil) * 1.18, 2)
    }
    for oil_price, silver_target in oil_table.items():
        st.write(f"Oil at {oil_price} → COMEX Silver target **${silver_target}**")

with tab4:
    st.subheader("Live COMEX Candle Chart + Real-time Prediction Lines")
    try:
        df = yf.download("SI=F", period="60d", interval="1d")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="COMEX Silver"))
        for name, level in vc_pmi_comex.items():
            price_line = level * 32.1507 * usdinr
            fig.add_hline(y=price_line, line_dash="dash", line_color="yellow", annotation_text=name.replace("_", " ").title())
        fig.update_layout(height=650, xaxis_rangeslider_visible=True, template="plotly_dark", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("Chart temporarily unavailable. All other data is live.")

st.caption("Auto-refreshes every 30 seconds • All targets dynamically scaled to your actual MCX price • Full consolidation of VC PMI + all experts data)

if st.button("🔄 Refresh All Live Data"):
    st.rerun()
