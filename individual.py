import math
from statistics import mean


class Individual:
    def __init__(self, expression, training_data=None):
        self._expression = expression
        self._training_data = training_data
        self._fitness = None

    def __str__(self):
        return self._expression.__str__()

    __repr__ = __str__

    def __eq__(self, other_ind):
        return self.expression == other_ind.expression

    def __lt__(self, other_ind):
        return self.fitness < other_ind.fitness

    def __hash__(self):
        return hash(str(self))

    @property
    def expression(self):
        return self._expression

    def _sq_err(self, x, y):
        try:
            return (y - self._expression.evaluate(x)) ** 2
        except OverflowError:
            return math.inf

    @property
    def fitness(self):
        """Return the fitness of this individual"""
        # Compute fitness if it hasn't been computed previously
        if self._fitness is None:
            sq_errs = [self._sq_err(x, y) for x, y in self._training_data.items()]
            self._fitness = mean(sq_errs)
        return self._fitness

    def train(self, training_data):
        self._training_data = training_data
