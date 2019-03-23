import math
from statistics import mean


class Individual:
    def __init__(self, expression):
        self._expression = expression
        self._fitness = None

    def __str__(self):
        return self._expression.__str__()

    __repr__ = __str__

    def _sq_err(self, x, y):
        try:
            return (y - self._expression.evaluate(x)) ** 2
        except OverflowError:
            return math.inf

    def fitness(self, training_data):
        # sq_errs = [(y - self._expression.evaluate(x)) ** 2 for x, y in training_data.items()]
        sq_errs = [self._sq_err(x, y) for x, y in training_data.items()]
        self._fitness = mean(sq_errs)
        return self._fitness
