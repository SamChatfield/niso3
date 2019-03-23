import initialisation

MAX_DEPTH = 10

class GP:
    def __init__(self, lambda_, training_data, init_method='growth'):
        self._population = initialisation.INIT_METHODS[init_method](lambda_, 10)

    def step(self):
        pass
