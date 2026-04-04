def regime(vol, usd_trend):

    if vol < 0.015 and usd_trend < 0:
        return "Expansion"
    elif vol > 0.03:
        return "Stress"
    return "Neutral"
