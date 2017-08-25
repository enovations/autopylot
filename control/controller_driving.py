import math

import __conf__
from control import controller_traffic

old_v = 0


def get_speed(r):
    global old_v

    if r == 0:
        return controller_traffic.speed_limit

    v = math.sqrt(__conf__.ar_max * abs(r))
    v = min(v, __conf__.max_speed)

    return v

    if abs(v) > abs(old_v):
        old_v = v * __conf__.acceleration_factor
    else:
        old_v = v * __conf__.deceleration_factor

    return old_v
