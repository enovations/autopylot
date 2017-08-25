from collections import deque

from control import controller_traffic


def path_from_to(start, stop):
    # BFS
    to_check = deque()
    to_check.append((start, [], [start]))  # current node, turns, path
    seen = set()

    while len(to_check) > 0:
        current, turns, path = to_check.popleft()

        if stop in controller_traffic.splits[current]:
            turns.append(controller_traffic.splits[current].index(stop))
            path.append(stop)
            return turns, path

        for option in controller_traffic.splits[current]:
            if option not in seen:
                to_check.append((option, turns + [controller_traffic.splits[current].index(option)], path+[option]))
                seen.add(option)

    return -1


class Navigation:
    def __init__(self):
        self.current_dest = None  # where we want to go

    def get_split_direction(self, current_split):
        if current_split == self.current_dest:
            self.current_dest = None
            return 0
        turns, path = path_from_to(current_split, self.current_dest)
        return turns[0], path
