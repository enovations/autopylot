# initial traffic conditions
speed_limit = 0.7

razcepi = [
    ('lams', ('parkirisce', 'obvoznica')),
    ('lams', ('parkirisce', 'obvoznica')),
    ('lams', ('parkirisce', 'obvoznica'))
]


def get_speed_limit():
    global speed_limit
    return speed_limit


def set_speed_limit(speed_limit_new):
    global speed_limit
    speed_limit = speed_limit_new
