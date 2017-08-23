import controller_traffic


def get_speed(w):
    max_speed = controller_traffic.get_speed_limit()
    if w == 0:
        speed = max_speed
    else:
        speed = max_speed * (1.0 / w)
    # TODO: Filter when ziga is done with filter
    return speed
