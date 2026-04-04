from xgboost import XGBRegressor

def train_xgb(X, y):
    model = XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05
    )
    model.fit(X, y)
    return model
