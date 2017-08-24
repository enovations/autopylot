import controller_traffic
from collections import deque


def path_from_to(start, stop):
    # BFS
    to_check = deque()
    to_check.append((controller_traffic.splits[start], [], [start]))  # current node, turns, nodes

    while len(to_check) > 0:
        options, turns, nodes = to_check.popleft()

        if stop in options:
            turns.append(options.index(stop))
            nodes.append(stop)
            return turns, nodes

        for i in range(len(options)):
            to_check.append((controller_traffic.splits[options[i]], turns + [i], nodes + [options[i]]))

    return -1


class Navigation:
    def __init__(self):
        self.current_dest = 'left'  # where we want to go
        self.location = None  # where we are

    def get_split_direction(self, current_split):
        if self.current_dest == 'left': return 0
        return 0
        # global location
        # global current_dest
        # location = current_split
        # return path_from_to(current_split, current_dest)
