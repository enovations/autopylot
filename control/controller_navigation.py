from collections import deque

from control import controller_traffic


def path_from_to(start, stop):
    # BFS
    to_check = deque()
    to_check.append((start, []))  # current node, turns
    seen = set()

    while len(to_check) > 0:
        current, turns = to_check.popleft()

        if stop in controller_traffic.splits[current]:
            turns.append(controller_traffic.splits[current].index(stop))
            return turns

        for option in controller_traffic.splits[current]:
            if option not in seen:
                to_check.append((option, turns + [controller_traffic.splits[current].index(option)]))
                seen.add(option)

    return -1


class Navigation:
    def __init__(self):
        self.current_dest = 'hodnik'  # where we want to go

    def get_split_direction(self, current_split):
        if current_split == self.current_dest:
            self.current_dest = None
            return 0
        return path_from_to(current_split, self.current_dest)[0]
