def position_size(vol, target_vol):
    if vol == 0:
        return 1
    return min(1, target_vol / vol)
