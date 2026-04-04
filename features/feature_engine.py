import pandas as pd
import numpy as np

def build_features(df):

    returns = df.pct_change()

    features = pd.DataFrame(index=df.index)

    features["silver_ret"] = returns["silver"]
    features["gold_ratio"] = df["gold"] / df["silver"]
    features["oil_beta"] = returns["oil"].rolling(10).mean()
    features["usd_trend"] = df["usdinr"].rolling(20).mean()

    features["volatility"] = returns["silver"].rolling(20).std()

    features = features.dropna()
    target = returns["silver"].shift(-1).loc[features.index]

    return features, target
