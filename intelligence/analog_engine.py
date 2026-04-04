import numpy as np

def analog_score(returns):
    similarity = np.corrcoef(returns[-60:], returns[-120:-60])[0,1]
    return similarity
