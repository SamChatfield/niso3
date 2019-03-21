import math
import operator

from collections import namedtuple

import sexpdata


def _from_string(expr_str):
    expr = sexpdata.loads(expr_str)
    print(f'from_string returns: {expr}')
    return expr


def _ifleq(a, b, x, y):
    return x if a <= b else y


Function = namedtuple('Function', ['func', 'args'])
DATA_FUNCS = ['data', 'diff', 'avg']
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
    'data': None,
    'diff': None,
    'avg': None,
}


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
        if self._function:
            func, args = self._function
            return f'{func} of {list(map(str, args))}'
        elif self._terminal:
            return f'{self._terminal}'
        else:
            raise Exception('Expression was neither a function nor a terminal')


    __repr__ = __str__

    def evaluate(self, x=None):
        if self._function:
            func, args = self._function
            print(f'func = {func}, args = {args}')
            evaluated_args = [arg.evaluate(x) for arg in args]
            print(f'evaluated_args = {evaluated_args}')

            # Compute the result catching any math domain errors or complex results
            try:
            res = func(*evaluated_args)
            print(f'res = {res}')
                if isinstance(res, complex):
                    return 0
            return res
            except ValueError as err:
                if 'math domain error' in str(err):
                    return 0
                raise err
        elif self._terminal:
            return self._terminal
        else:
            raise Exception('Expression was neither a function nor a terminal')

    eval = evaluate
