import controller_traffic


def get_speed(r):
    max_speed = controller_traffic.get_speed_limit()
    if r == 0:
        speed = max_speed
    else:
        speed = max_speed * r * 0.15
    # TODO: Filter when ziga is done with filter
    return min(speed, max_speed)
