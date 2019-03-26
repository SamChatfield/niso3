import random
import sys
import math

from expression import FUNC_MAP, Expression
from individual import Individual

# FUNCTION_SET = list(FUNC_MAP.values())
FUNCTION_SET = list(FUNC_MAP.keys())


def _random_function():
    func_str = random.choice(FUNCTION_SET)
    return func_str, FUNC_MAP[func_str]


def _random_terminal():
    return random.uniform(-1.0, 1.0)


def random_expression(max_depth=5, p_early_terminal=0):
    def _random_expression(depth=0):
        early_terminal = p_early_terminal != 0 and random.random() < p_early_terminal
        if early_terminal or depth == max_depth:
            # Add terminal
            return _random_terminal()
        # Add function
        func_str, func = _random_function()
        rand_args = [_random_expression(depth + 1) for i in range(func.arity)]
        return [func_str, *rand_args]

    # rand_expr = _random_expression()
    rand_expr = Expression(_random_expression())
    return rand_expr


def full(lambda_, depth):
    pop = []
    for i in range(lambda_):
        ind = Individual(random_expression(depth))
        # print(f'ind i={i}:\n{ind}\n', file=sys.stderr)
        pop.append(ind)
    return pop


def growth(lambda_, max_depth, p_early_terminal=0.1):
    pop = []
    for i in range(lambda_):
        ind = Individual(random_expression(max_depth, p_early_terminal))
        # print(f'ind i={i}:\n{ind}\n', file=sys.stderr)
        pop.append(ind)
    return pop


def half_and_half(lambda_, max_depth):
    assert lambda_ >= 2 * (max_depth - 1)
    part_size = math.ceil(lambda_ / (2 * (max_depth - 1)))
    pop = []
    for n in range(2, max_depth + 1):
        pop += full(part_size, n)
        pop += growth(part_size, n)
    return pop[:lambda_]

INIT_METHODS = {
    'full': full,
    'growth': growth,
    'half_and_half': half_and_half
}
