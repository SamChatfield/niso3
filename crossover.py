import random
import sys
from typing import Tuple

from individual import Individual


def branch_swap(ind1: Individual, ind2: Individual) -> Tuple[Individual, Individual]:
    ind1_idx = random.randrange(ind1.expression.length)
    ind2_idx = random.randrange(ind2.expression.length)
    print(f'i1 = {ind1_idx}, i2 = {ind2_idx}', file=sys.stderr)

    ind1_subtree = ind1.expression.subtree_at(ind1_idx)
    ind2_subtree = ind2.expression.subtree_at(ind2_idx)
    print(f'sub1:\n{ind1_subtree}\nsub2:\n{ind2_subtree}\n', file=sys.stderr)

    ind3 = Individual(ind1.expression.replace_subtree(ind1_idx, ind2_subtree))
    ind4 = Individual(ind2.expression.replace_subtree(ind2_idx, ind1_subtree))
    print(f'ind3:\n{ind3}\nind4:\n{ind4}\n', file=sys.stderr)

    return ind3, ind4


def matched_one_point(ind1, ind2):
    pass


CROSSOVER_METHODS = {
    'branch_swap': branch_swap,
    'matched_one_point': matched_one_point
}
