import math
from statistics import mean


class Individual:
    def __init__(self, expression, training_data=None):
        self._expression = expression
        self._training_data = training_data
        self._fitness = None
        self._expression_str_saved = None

    def __str__(self):
        return self._expression.__str__()

    __repr__ = __str__

    def __eq__(self, other_ind):
        return self.expression == other_ind.expression

    def __lt__(self, other_ind):
        return self.fitness < other_ind.fitness

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
            self._expression_str_saved = str(self._expression)
        # Make sure that the expression hasn't changed since we calculated fitness
        assert str(self._expression) == self._expression_str_saved
        return self._fitness

    def train(self, training_data):
        self._training_data = training_data
