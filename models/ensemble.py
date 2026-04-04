import numpy as np

def ensemble_prediction(arima_p, xgb_p, lstm_p, vol):

    weights = {
        "arima": 0.25,
        "xgb": 0.40,
        "lstm": 0.35
    }

    pred = (
        weights["arima"] * arima_p +
        weights["xgb"] * xgb_p +
        weights["lstm"] * lstm_p
    )

    confidence = 1 / (1 + vol)

    return pred, confidence
