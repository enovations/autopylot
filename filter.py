from collections import deque
import __conf__


class Filter:
    def __init__(self):
        self.q = deque([(0, 0) for _ in range(10)])
        self.weights = [1, 1, 2, 3, 3, 3, 4, 5, 5, 6]

    def get(self, new_r, new_s):
        w = self.r_to_w(new_r)
        self.q.popleft()
        self.q.append((w, new_s))
        return self.calculate()

    def calculate(self):
        weighted = [self.weights[i] * tupl[1] for i, tupl in enumerate(self.q)]
        max = sum(weighted)
        weighted = [i / max for i in weighted]
        return sum(weighted[i] * tupl[0] for i, tupl in enumerate(self.q)) / len(weighted)

    @staticmethod
    def r_to_w(r):
        print(r)
        if r == 0: return 0
        r = float(r) * __conf__.meter_to_pixel_ratio  # convert to meters
        return __conf__.v / r
