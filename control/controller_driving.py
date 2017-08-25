import math

import __conf__
from control import controller_traffic

old_v = 0


def get_speed(r):
    global old_v

    if r == 0:
        return controller_traffic.speed_limit

    v = math.sqrt(__conf__.ar_max * abs(r))
    v = min(v, controller_traffic.speed_limit)

    if abs(v) > abs(old_v):
        old_v = (old_v * (1 - __conf__.accel_filter_factor) + v * __conf__.accel_filter_factor)
    else:
        old_v = (old_v * (1 - __conf__.deccl_filter_factor) + v * __conf__.deccl_filter_factor)

    return old_v
