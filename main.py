import csv
import math
import sys
from pprint import pprint
from statistics import mean

import sexpdata

import arg_parser
from expression import Expression


# TODO: change to parameter v instead of e
def mod_abs_floor(e, n, x):
    return abs(math.floor(eval_expr(e, n, x))) % n


def data(e, n, x):
    return x[mod_abs_floor(e, n, x)]


def eval_expr(expr, n, x):
    """Evaluate s-expression and return its value"""
    print('evalexpr of {} with type {}'.format(expr, type(expr)), file=sys.stderr)
    if type(expr) == list:
        if type(expr[0]) == sexpdata.Symbol:
            op = expr[0].value()
            print('Operation {} for args {}'.format(op, expr[1:]), file=sys.stderr)

            if (op == 'add'):
                return eval_expr(expr[1], n, x) + eval_expr(expr[2], n, x)
            elif (op == 'sub'):
                return eval_expr(expr[1], n, x) - eval_expr(expr[2], n, x)
            elif (op == 'mul'):
                return eval_expr(expr[1], n, x) * eval_expr(expr[2], n, x)
            elif (op == 'div'):
                arg2 = eval_expr(expr[2], n, x)
                if arg2 == 0:
                    return 0
                else:
                    return eval_expr(expr[1], n, x) / arg2
            elif (op == 'pow'):
                try:
                    res = eval_expr(expr[1], n, x) ** eval_expr(expr[2], n, x)
                    if isinstance(res, complex):
                        return 0
                    else:
                        return res
                except (ZeroDivisionError, ValueError, OverflowError, TypeError):
                    return 0
            elif (op == 'sqrt'):
                arg = eval_expr(expr[1], n, x)
                print(f'sqrt arg: {arg}, type:{type(arg)}', file=sys.stderr)
                if arg < 0:
                    return 0
                else:
                    res = math.sqrt(arg)
                    if isinstance(res, complex):
                        return 0
                    else:
                        return res
            elif (op == 'log'):
                arg = eval_expr(expr[1], n, x)
                if arg <= 0:
                    return 0
                else:
                    res = math.log2(arg)
                    if isinstance(res, complex):
                        return 0
                    else:
                        return res
            elif (op == 'exp'):
                try:
                    res = math.exp(eval_expr(expr[1], n, x))
                    if isinstance(res, complex):
                        return 0
                    else:
                        return res
                except (ZeroDivisionError, ValueError, OverflowError, TypeError):
                    return 0
            elif (op == 'max'):
                arg1 = eval_expr(expr[1], n, x)
                arg2 = eval_expr(expr[2], n, x)
                return max(arg1, arg2)
            elif (op == 'ifleq'):
                arg1 = eval_expr(expr[1], n, x)
                arg2 = eval_expr(expr[2], n, x)
                if (arg1 <= arg2):
                    return eval_expr(expr[3], n, x)
                else:
                    return eval_expr(expr[4], n, x)
            elif (op == 'data'):
                return data(expr[1], n, x)
            elif op == 'diff':
                data1 = data(expr[1], n, x)
                data2 = data(expr[2], n, x)
                return data1 - data2
            elif op == 'avg':
                k = mod_abs_floor(expr[1], n, x)
                l = mod_abs_floor(expr[2], n, x)
                start = min(k, l)
                end = max(k, l)
                try:
                    return (1 / abs(k - l)) * sum(x[start:end])
                except (ZeroDivisionError, ValueError, OverflowError, TypeError):
                    return 0
            else:
                print('Invalid symbol {}'.format(expr[0]), file=sys.stderr)
                sys.exit(1)
        else:
            print('Evaluate singleton {}'.format(expr[0]), file=sys.stderr)
            return eval_expr(expr[0], n, x)
    else:
        print('Return terminal value {}'.format(expr), file=sys.stderr)
        return expr


def question1(expr, n, x):
    expr = Expression(expr)
    return expr.evaluate(x)


def question1_old(expr, n, x):
    expr_parsed = sexpdata.loads(expr)
    print('expr_parsed:', file=sys.stderr)
    pprint(expr_parsed, stream=sys.stderr, indent=4)
    print(f'x: {x}, tx: {type(x)}', file=sys.stderr)
    return eval_expr(expr_parsed, n, x)


def parse_data(data):
    training_data = {}
    with open(data) as f:
        for row in csv.reader(f, delimiter='\t'):
            *x, y = row
            x = tuple(map(float, x))
            y = float(y)
            training_data[x] = y
    return training_data


def calc_fitness(expr, n, m, training_data):
    sq_errs = [(y - eval_expr(expr, n, x)) ** 2 for x, y in training_data.items()]
    fitness = mean(sq_errs)
    return fitness


def question2(expr, n, m, data):
    expr_parsed = sexpdata.loads(expr)
    print('expr_parsed:', file=sys.stderr)
    pprint(expr_parsed, stream=sys.stderr, indent=4)
    training_data = parse_data(data)
    return calc_fitness(expr_parsed, n, m, training_data)


def main():
    print('main', file=sys.stderr)
    args = arg_parser.parse()
    print('Question:\n{}\n'.format(args.question), file=sys.stderr)
    print('Expr:\n{}\n'.format(args.expr), file=sys.stderr)
    print('N:\n{}\n'.format(args.n), file=sys.stderr)
    print('X:\n{}\n'.format(args.x), file=sys.stderr)

    if args.question == 1:
        print('Q1:\n', file=sys.stderr)
        print(question1(args.expr, args.n, args.x))
    elif args.question == 2:
        print('question 2', file=sys.stderr)
        print(question2(args.expr, args.n, args.m, args.data))
    elif args.question == 3:
        print('question 3', file=sys.stderr)
        pass
    else:
        print('Error: Invalid question number supplied', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
