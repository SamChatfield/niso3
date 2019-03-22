import csv
import sys
from statistics import mean

import arg_parser
from expression import Expression


def question1(expr, x):
    expr = Expression(expr)
    return expr.evaluate(x)


def parse_data(data):
    training_data = {}
    with open(data) as f:
        for row in csv.reader(f, delimiter='\t'):
            *x, y = row
            x = tuple(map(float, x))
            y = float(y)
            training_data[x] = y
    return training_data


def calc_fitness(expr, training_data):
    sq_errs = [(y - expr.evaluate(x)) ** 2 for x, y in training_data.items()]
    fitness = mean(sq_errs)
    return fitness


def question2(expr, data):
    expr = Expression(expr)
    training_data = parse_data(data)
    return calc_fitness(expr, training_data)


def main():
    print('main', file=sys.stderr)
    args = arg_parser.parse()
    print('Question:\n{}\n'.format(args.question), file=sys.stderr)
    print('Expr:\n{}\n'.format(args.expr), file=sys.stderr)
    print('N:\n{}\n'.format(args.n), file=sys.stderr)
    print('X:\n{}\n'.format(args.x), file=sys.stderr)

    if args.question == 1:
        print('Q1:\n', file=sys.stderr)
        print(question1(args.expr, args.x))
    elif args.question == 2:
        print('question 2', file=sys.stderr)
        print(question2(args.expr, args.data))
    elif args.question == 3:
        print('question 3', file=sys.stderr)
    else:
        print('Error: Invalid question number supplied', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
