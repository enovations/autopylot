from collections import deque


class Filter:
    def __init__(self, weights):
        self.q = deque([0 for _ in range(len(weights))])
        self.weights = weights

    def get(self, new_value):
        self.q.popleft()
        self.q.append(new_value)
        return self.calculate()

    def calculate(self):
        return sum([e*self.weights[i] for i, e in enumerate(self.q)]) / sum(self.weights)

    @staticmethod
    def r_to_w(r, v):
        if r == 0:
            return 0
        return v / r
