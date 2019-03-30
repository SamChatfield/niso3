import logging
import queue
import time
import threading
from math import floor

import crossover
import initialisation
import mutation
import selection


class GP:
    def __init__(self, lambda_, training_data,
                 best_individuals=None,
                 init_method='half_and_half', max_depth=5,
                 selection_method='truncation', parent_proportion=0.25,
                 crossover_method='branch_swap',
                mutation_method='branch_replacement', mutation_target='non_parents', mutation_rate=0.2):
        self._lambda = lambda_
        self._training_data = training_data
        self._best_individuals = best_individuals if best_individuals is not None else queue.LifoQueue()
        assert isinstance(self._best_individuals, queue.LifoQueue)

        self._population = initialisation.INIT_METHODS[init_method](lambda_, max_depth)
        assert(len(self._population) == len(set(self._population)))

        # Train the population
        for ind in self._population:
            ind.train(self._training_data)

        # Sort the population
        self._population.sort()

        self._max_depth = max_depth

        self._selection_method = selection_method
        self._num_parents = max(2, floor(lambda_ * parent_proportion))

        self._crossover_method = crossover_method

        self._mutation_method = mutation_method
        self._mutation_target = mutation_target
        self._mutation_rate = mutation_rate

    def generation(self):
        # Use the selection method to get pairs of parents and the individuals not selected
        (parent_pairs, non_parents) = selection.SELECTION_METHODS[self._selection_method](self._num_parents, self._population)

        # Generate children using crossover
        tc0 = time.time()
        children = []
        for ind1, ind2 in parent_pairs:
            (child1, child2) = crossover.CROSSOVER_METHODS[self._crossover_method](ind1, ind2)
            children += [child1, child2]
        logging.debug('CROSSOVER TIME = %s', time.time() - tc0)

        # Apply mutation
        tm0 = time.time()
        if self._mutation_target == 'children':
            mut_target_inds = children
        elif self._mutation_target == 'non_parents':
            mut_target_inds = non_parents
        elif self._mutation_target == 'children_and_non_parents':
            mut_target_inds = children + non_parents
        else:
            raise Exception(f'Invalid mutation target: {self._mutation_target}')
        mutated_inds = [mutation.MUTATION_METHODS[self._mutation_method](i, self._max_depth, self._mutation_rate) for i in mut_target_inds]
        mutated_inds = list(filter(None.__ne__, mutated_inds))
        logging.debug('MUTATION TIME = %s', time.time() - tm0)

        # Add the results of crossover and mutation together
        new_pop = children + mutated_inds

        # Train new individuals
        for ind in new_pop:
            ind.train(self._training_data)

        tsort0 = time.time()
        # Add the new individuals to the population
        self._population += new_pop
        # Remove duplicates from the population
        self._population = list(set(self._population))

        # Sort the population again
        self._population.sort()
        # Set the final population for this generation to be the lambda best individuals
        self._population = self._population[:self._lambda]
        logging.debug('FITNESSES: %s', [ind.fitness for ind in self._population])
        logging.debug('END SORTING TIME = %s', time.time() - tsort0)

        self._best_individuals.put(self._population[0])
        logging.debug('BEST IND FOR GEN (fitness = %s):\n%s', self._population[0].fitness, self._population[0])

    def run(self, generations):
        for i in range(generations):
            self.generation()
            logging.debug('GEN %s', i)
            logging.debug('FITNESSES: %s', sorted([ind.fitness for ind in self._population]))
            logging.debug('LENGTHS: %s', sorted([len(ind.expression) for ind in self._population]))
        return self._best_individuals.get()


def _run_gp_thread(stop_event, results_queue, lambda_, training_data, gp_kwargs):
    gp_kwargs = gp_kwargs if gp_kwargs is not None else {}
    gp_obj = GP(lambda_, training_data, results_queue, **gp_kwargs)
    i = 0
    while not stop_event.is_set() and i < 1000:
        gp_obj.generation()


def run_gp(time_budget, lambda_, training_data, gp_kwargs=None):
    best_individuals = queue.LifoQueue()

    gp_thread_stop = threading.Event()
    gp_thread = threading.Thread(
        target=_run_gp_thread,
        args=(gp_thread_stop, best_individuals, lambda_, training_data, gp_kwargs),
        daemon=True
    )
    gp_thread.start()
    time.sleep(time_budget)
    gp_thread_stop.set()

    best_individual = best_individuals.get(timeout=10.0)
    return best_individual
