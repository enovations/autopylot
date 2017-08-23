import controller_traffic
import math


def get_speed(r, filter):
    max_speed = controller_traffic.get_speed_limit()
    if r == 0:
        speed = max_speed
    else:
        speed = max_speed * abs(r) * 0.3

    v = filter.get([min(math.sqrt(speed), max_speed)])
    return v
