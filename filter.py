from collections import deque
import __conf__


class Filter:
    def __init__(self, queue_size, weights):
        self.q = deque([[0 for _ in range(len(weights))] for _ in range(queue_size)])
        self.weights = weights

    def get(self, new_values):
        self.q.popleft()
        self.q.append(new_values)
        return self.calculate()

    def calculate(self):
        return [sum(elements[i] * self.weights[j] for j, elements in enumerate(self.q)) / sum(self.weights) / sum(self.weights) for i in range(len(self.weights))]
        # return sum(tupl[0]*self.weights[i] for i, tupl in enumerate(self.q)) / sum(self.weights), sum(tupl[2]*__conf__.position_gain*self.weights[i] for i, tupl in enumerate(self.q)) / sum(self.weights)

    @staticmethod
    def r_to_w(r):
        if r == 0: return 0
        r = float(r) * __conf__.meter_to_pixel_ratio  # convert to meters
        return __conf__.v / r
