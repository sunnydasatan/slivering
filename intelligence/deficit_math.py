def deficit_pressure(deficit_moz=67, production=820):
    ratio = deficit_moz / production
    uplift = ratio * 10
    return uplift
