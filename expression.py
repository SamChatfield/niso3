import logging
import math
import operator
from collections import namedtuple
from copy import deepcopy

import sexpdata


def _from_string(expr_str):
    expr = sexpdata.loads(expr_str)
    # print(f'from_string returns: {expr}', file=sys.stderr)
    return expr


def _ifleq(a, b, x, y):
    return x if a <= b else y


def _mod_abs_floor(a, n):
    return abs(math.floor(a)) % n


def _data(a, x):
    n = len(x)
    # print(f'_data: a = {a}, n = {n}, x = {x}', file=sys.stderr)
    assert isinstance(x, tuple)
    # assert 0 < a < n
    return x[_mod_abs_floor(a, n)]


def _diff(a, b, x):
    assert isinstance(x, tuple)
    data_a = _data(a, x)
    data_b = _data(b, x)
    return data_a - data_b


def _avg(a, b, x):
    assert isinstance(x, tuple)
    k = _mod_abs_floor(a, len(x))
    l = _mod_abs_floor(b, len(x))
    start = min(k, l)
    end = max(k, l)
    return (1 / abs(k - l)) * sum(x[start:end])


Function = namedtuple('Function', ['func', 'arity'])
FUNC_MAP = {
    # Math functions
    'add': Function(operator.add, 2),
    'sub': Function(operator.sub, 2),
    'mul': Function(operator.mul, 2),
    'div': Function(operator.truediv, 2),
    'pow': Function(pow, 2),
    'sqrt': Function(math.sqrt, 1),
    'log': Function(math.log2, 1),
    'exp': Function(math.exp, 1),
    'max': Function(max, 2),
    'ifleq': Function(_ifleq, 4),
    # Data functions
    'data': Function(_data, 1),
    'diff': Function(_diff, 2),
    'avg': Function(_avg, 2),
}
# The subset of functions which require x being passed as an additional argument
DATA_FUNCS = list(FUNC_MAP.values())[-3:]


class Expression:
    def __init__(self, expr):
        # An expression can be either a function or a terminal
        self._function = None
        self._args = None
        self._function_name = None
        self._terminal = None

        if expr is None:
            raise ValueError('Expr cannot be None')

        # If expr is a string, parse the s-expression
        if isinstance(expr, str):
            expr = _from_string(expr)

        # If expr represents a function
        if isinstance(expr, list):
            while len(expr) == 1:
                expr = expr[0]
            func_name, *args = expr
            # Extract the string function name if this is an sexpdata Symbol
            if isinstance(func_name, sexpdata.Symbol):
                func_name = func_name.value()
            self._function = FUNC_MAP[func_name]
            self._args = [Expression(arg) for arg in args]
            self._function_name = func_name
            # Check that the number of args and the function arity match
            assert self._function.arity == len(self._args)
        # If expr represents a terminal
        else:
            self._terminal = expr

        # An expression cannot be both a function and a terminal
        assert not (self._function and self._terminal)

    def __len__(self):
        if self._function is not None:
            return 1 + sum([len(child) for child in self._args])
        if self._terminal is not None:
            return 1
        raise Exception('Expression was neither a function nor a terminal')

    def __str__(self):
        if self._function is not None:
            args_str = ' '.join(arg.__str__() for arg in self._args)
            return f'({self._function_name} {args_str})'
        if self._terminal is not None:
            return f'{self._terminal}'
        raise Exception('Expression was neither a function nor a terminal')

    __repr__ = __str__

    def __eq__(self, other_expr):
        return self.__str__() == str(other_expr)

    @property
    def height(self):
        if self._function is not None:
            return 1 + max([child.height for child in self._args])
        if self._terminal is not None:
            return 0
        raise Exception('Expression was neither a function nor a terminal')

    def expand(self):
        if self._function is not None:
            return [self._function.func, [arg.expand() for arg in self._args]]
        if self._terminal is not None:
            return self._terminal
        raise Exception('Expression was neither a function nor a terminal')

    def evaluate(self, x=None):
        if self._function is not None:
            func, _ = self._function
            # print(f'func = {func}, args = {self._args}', file=sys.stderr)

            # Evaluate the Expression's children
            evaluated_args = [arg.evaluate(x) for arg in self._args]

            # Add the input vector x as an additional argument for data functions
            if self._function in DATA_FUNCS:
                if x is None:
                    raise ValueError('Input vector x was None for an expression with data functions')
                evaluated_args.append(x)
            # print(f'evaluated_args = {evaluated_args}', file=sys.stderr)

            # Compute the result catching relevant math errors
            try:
                # Call the function
                # print(f'EVALUATE {func} for {evaluated_args}', file=sys.stderr)
                res = func(*evaluated_args)
                # print(f'res = {res}', file=sys.stderr)
                # For complex results return 0
                if isinstance(res, complex):
                    return 0
                # If the result is inf (operation overflowed) return 0
                if math.isinf(res):
                    return 0
                # If the result is NaN something has gone wrong
                if math.isnan(res):
                    raise Exception(f'Res gave NaN for func={func} and args={evaluated_args}')
                # Otherwise, return the result
                return res
            except (ZeroDivisionError, OverflowError):
                # If we have a division by 0 or a pow operation overflows return 0
                return 0
            except ValueError as err:
                # If we have a math domain error from e.g. sqrt(-1) return 0
                if 'math domain error' in str(err):
                    return 0
                raise err
        elif self._terminal is not None:
            return self._terminal
        else:
            raise Exception('Expression was neither a function nor a terminal')

    # Alias for evaluate
    eval = evaluate

    def subtree_at(self, idx):
        if idx >= self.__len__():
            raise ValueError(f'idx {idx} out of range for length {self.__len__()}')
        if idx == 0:
            return self
        for child in self._args:
            if idx == 1:
                return child
            if idx <= len(child):
                return child.subtree_at(idx - 1)
            idx -= len(child)
            # return child.subtree_at(idx - len(child))
        raise Exception(f'Nothing returned by subtree_at, self={self}, idx={idx}')

    def replace_subtree(self, idx, subtree):
        assert subtree is not None
        if idx >= self.__len__():
            raise ValueError(f'idx {idx} out of range for length {self.__len__()}')
        if idx == 0:
            return deepcopy(subtree)
        newtree = deepcopy(self)
        for i in range(len(newtree._args)):
            if idx == 1:
                newtree._args[i] = deepcopy(subtree)
                break
            elif idx <= len(newtree._args[i]):
                newtree._args[i] = newtree._args[i].replace_subtree(idx - 1, subtree)
                break
            else:
                idx -= len(newtree._args[i])
        return newtree
