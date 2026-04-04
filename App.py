import streamlit as st
from data.data_loader import load_market_data
from features.feature_engine import build_features
from models.arima_model import arima_forecast
from models.xgb_model import train_xgb
from models.lstm_model import train_lstm
from models.ensemble import ensemble_prediction
from intelligence.regime_detector import regime
from intelligence.deficit_math import deficit_pressure
from risk.risk_engine import position_size

st.set_page_config(layout="wide", page_title="OMEGA ASCENSION")

st.title("OMEGA ASCENSION — Autonomous Intelligence")

df = load_market_data()
X, y = build_features(df)

arima_p = arima_forecast(df["silver"])
xgb = train_xgb(X[:-1], y[:-1])
xgb_p = xgb.predict(X.tail(1))[0]

lstm = train_lstm(X[:-1], y[:-1])
lstm_p = lstm.predict(X.tail(1).values.reshape(1,X.shape[1],1))[0][0]

vol = X["volatility"].iloc[-1]

pred, conf = ensemble_prediction(arima_p, xgb_p, lstm_p, vol)

reg = regime(vol, X["usd_trend"].iloc[-1])
risk = position_size(vol, 0.18)

omega_score = pred * 100 * conf

col1, col2, col3 = st.columns(3)

col1.metric("Omega Score", round(omega_score,2))
col2.metric("Regime", reg)
col3.metric("Risk Allocation", round(risk,2))

st.line_chart(df["silver"])
