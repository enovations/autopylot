from collections import deque
import __conf__


class Filter:
    def __init__(self, weights, num_of_fields):
        self.q = deque([[0 for _ in range(num_of_fields)] for _ in range(len(weights))])
        self.weights = weights
        self.num_of_fields = num_of_fields

    def get(self, new_values):
        self.q.popleft()
        self.q.append(new_values)
        return self.calculate()

    def calculate(self):
        result = []
        for i in range(self.num_of_fields):
            vsota = sum([element[i] * self.weights[j] for j, element in enumerate(self.q)])
            result.append(vsota / sum(self.weights))
        return result

    @staticmethod
    def r_to_w(r, v):
        if r == 0:
            return 0
        return v / r
