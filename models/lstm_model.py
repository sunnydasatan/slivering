import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def train_lstm(X, y):

    X = np.array(X).reshape(len(X), X.shape[1], 1)

    model = Sequential([
        LSTM(32),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=5, verbose=0)

    return model
