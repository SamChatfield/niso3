import sys
import math
import operator

from collections import namedtuple

import sexpdata


def _from_string(expr_str):
    expr = sexpdata.loads(expr_str)
    print(f'from_string returns: {expr}', file=sys.stderr)
    return expr


def _ifleq(a, b, x, y):
    return x if a <= b else y


def _mod_abs_floor(a, n):
    return abs(math.floor(a)) % n


def _data(a, x):
    n = len(x)
    print(f'_data: a = {a}, n = {n}, x = {x}', file=sys.stderr)
    assert isinstance(x, list)
    # assert 0 < a < n
    return x[_mod_abs_floor(a, n)]


def _diff(a, b, x):
    assert isinstance(x, list)
    data_a = _data(a, x)
    data_b = _data(b, x)
    return data_a - data_b


def _avg(a, b, x):
    assert isinstance(x, list)
    k = _mod_abs_floor(a, len(x))
    l = _mod_abs_floor(b, len(x))
    start = min(k, l)
    end = max(k, l)
    return (1 / abs(k - l)) * sum(x[start:end])


Function = namedtuple('Function', ['func', 'args'])
FUNC_MAP = {
    # Math functions
    'add': operator.add,
    'sub': operator.sub,
    'mul': operator.mul,
    'div': operator.truediv,
    'pow': pow,
    'sqrt': math.sqrt,
    'log': math.log2,
    'exp': math.exp,
    'max': max,
    'ifleq': _ifleq,
    # Data functions
    'data': _data,
    'diff': _diff,
    'avg': _avg,
}
# The subset of functions which require x being passed as an additional argument
DATA_FUNCS = list(FUNC_MAP.values())[-3:]


class Expression:
    def __init__(self, expr):
        # An expression can be either a function or a terminal
        self._function = None
        self._terminal = None

        # If expr is a string, parse the s-expression
        if isinstance(expr, str):
            expr = _from_string(expr)

        # If expr represents a function
        if isinstance(expr, list):
            while len(expr) == 1:
                expr = expr[0]
            func_name, *args = expr
            arg_exprs = [Expression(arg) for arg in args]
            self._function = Function(FUNC_MAP[func_name.value()], arg_exprs)
        # If expr represents a terminal
        else:
            self._terminal = expr

        # An expression cannot be both a function and a terminal
        assert not (self._function and self._terminal)

    def __str__(self):
        if self._function is not None:
            func, args = self._function
            return f'{func} of {list(map(str, args))}'
        if self._terminal is not None:
            return f'{self._terminal}'
        raise Exception('Expression was neither a function nor a terminal')

    __repr__ = __str__

    def evaluate(self, x=None):
        if self._function is not None:
            func, args = self._function
            print(f'func = {func}, args = {args}', file=sys.stderr)

            # Evaluate the Expression's children
            evaluated_args = [arg.evaluate(x) for arg in args]

            # Add the input vector x as an additional argument for data functions
            if func in DATA_FUNCS:
                evaluated_args.append(x)
            print(f'evaluated_args = {evaluated_args}', file=sys.stderr)

            # Compute the result catching relevant math errors
            try:
                # Call the function
                res = func(*evaluated_args)
                print(f'res = {res}', file=sys.stderr)
                # For complex results return 0
                if isinstance(res, complex):
                    return 0
                # Return the result
                return res
            except ZeroDivisionError:
                return 0
            except ValueError as err:
                if 'math domain error' in str(err):
                    return 0
                raise err
            except OverflowError as err:
                if 'math range error' in str(err):
                    return 0
                raise err
        elif self._terminal is not None:
            return self._terminal
        else:
            raise Exception('Expression was neither a function nor a terminal')

    eval = evaluate
