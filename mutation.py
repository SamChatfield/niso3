import sys
from random import randrange

from individual import Individual
from initialisation import growth


def branch_replacement(ind: Individual, max_depth) -> Individual:
    # Choose the index of the subtree to replace
    repl_idx = randrange(len(ind.expression))
    # print(f'REPL_IDX = {repl_idx} from len = {len(ind.expression)} from ind = {ind.expression}')
    new_expr = growth(1, max_depth)[0].expression
    assert new_expr is not None

    new_ind = Individual(ind.expression.replace_subtree(repl_idx, new_expr))
    assert new_ind.expression is not None

    return new_ind


MUTATION_METHODS = {
    'none': lambda i: i,
    'branch_replacement': branch_replacement
}
