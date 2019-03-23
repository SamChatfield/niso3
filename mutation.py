from random import randrange

from individual import Individual
from initialisation import growth


def branch_replacement(ind: Individual) -> Individual:
    repl_idx = randrange(len(ind.expression))
    repl_expr = growth(1, 10)[0].expression

    new_ind = Individual(ind.expression.replace_subtree(repl_idx, repl_expr))

    return new_ind


MUTATION_METHODS = {
    'branch_replacement': branch_replacement
}
