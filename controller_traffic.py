# initial traffic conditions
speed_limit = 0.5


def get_speed_limit():
    global speed_limit
    return speed_limit


def set_speed_limit(speed_limit_new):
    global speed_limit
    speed_limit = speed_limit_new
