import sys
from math import floor

import crossover
import initialisation
import mutation
import selection


class GP:
    def __init__(self, lambda_, training_data, best_individuals=[],
        init_method='growth', max_depth=5,
        selection_method='truncation', parent_proportion=0.25,
        crossover_method='branch_swap',
        mutation_method='branch_replacement'
    ):
        self._lambda = lambda_
        self._training_data = training_data
        self._best_individuals = best_individuals

        self._population = initialisation.INIT_METHODS[init_method](lambda_, max_depth)

        self._max_depth = max_depth

        self._selection_method = selection_method
        self._num_parents = max(2, floor(lambda_ * parent_proportion))

        self._crossover_method = crossover_method

        self._mutation_method = mutation_method

    def generation(self):
        # Train the population
        for ind in self._population:
            ind.train(self._training_data)
        # print(f'Trained pop:\n{self._population}', file=sys.stderr)

        # Sort the population
        sorted_pop = sorted(self._population)
        # print(f'Sorted pop\n{sorted_pop}', file=sys.stderr)

        # Use the selection method to get a list of breeding pairs [(Individual, Individual)]
        breeding_pairs = selection.SELECTION_METHODS[self._selection_method](self._num_parents, sorted_pop)
        # print(f'Breeding pairs:\n{breeding_pairs}', file=sys.stderr)

        # Generate children using crossover
        children = []
        for ind1, ind2 in breeding_pairs:
            child1, child2 = crossover.CROSSOVER_METHODS[self._crossover_method](ind1, ind2)
            children += [child1, child2]
        # print(f'Children\n{children}', file=sys.stderr)

        # Add children to the population
        # pop_with_children = sorted_pop + children

        # Apply mutation
        # mutated_pop = [mutation.MUTATION_METHODS[self._mutation_method](i) for i in pop_with_children]
        mutated_children = [mutation.MUTATION_METHODS[self._mutation_method](i, self._max_depth) for i in children]
        # Train mutated population
        # for ind in mutated_pop:
        #     ind.train(self._training_data)
        for ind in mutated_children:
            ind.train(self._training_data)

        new_pop = sorted_pop + mutated_children

        # Sort the population again
        # Set the final population for this generation to be the lambda best individuals
        # self._population = sorted(mutated_pop)[:self._lambda]
        self._population = sorted(new_pop)[:self._lambda]

        # print(f'BEST IND FOR GEN (fitness = {self._population[0].fitness}):\n{self._population[0]}', file=sys.stderr)
        # print(f'BEST FITNESS FOR GEN = {self._population[0].fitness}', file=sys.stderr)
        self._best_individuals.append(self._population[0])

    def run(self, generations):
        for i in range(generations):
            self.generation()
            print(f'GEN {i}', file=sys.stderr)
            print(f'FITNESSES: {sorted([i.fitness for i in self._population])}', file=sys.stderr)
            print(f'LENGTHS: {sorted([len(i.expression) for i in self._population])}', file=sys.stderr)
