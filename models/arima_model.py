from statsmodels.tsa.arima.model import ARIMA

def arima_forecast(series):
    model = ARIMA(series, order=(2,1,2))
    fit = model.fit()
    forecast = fit.forecast()[0]
    return forecast
