import controller_traffic


def get_speed(r, filter):
    max_speed = controller_traffic.get_speed_limit()
    if r == 0:
        speed = max_speed
    else:
        speed = max_speed * abs(r) * 0.15

    v = filter.get([min(speed, max_speed)])
    return v
