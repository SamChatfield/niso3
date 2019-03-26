import csv
import sys
import time
from statistics import mean
from threading import Event, Thread

import arg_parser
from expression import Expression
from gp import GP
from individual import Individual


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


def question2(expr, data):
    ind = Individual(Expression(expr))
    training_data = parse_data(data)
    ind.train(training_data)
    return ind.fitness


def gp_thread(stop_event, lambda_, training_data, best_individuals):
    gpobj = GP(lambda_, training_data, best_individuals)
    i = 0
    while not stop_event.is_set() and i < 1000:
        gpobj.generation()
        # print(f'GEN {i}', file=sys.stderr)
        # print(f'FITNESSES: {sorted([i.fitness for i in gpobj._population])}', file=sys.stderr)
        # print(f'LENGTHS: {sorted([len(i.expression) for i in gpobj._population])}', file=sys.stderr)
        i += 1


def question3(lambda_, data, time_budget):
    start_time = time.time()
    training_data = parse_data(data)
    best_individuals = []
    thread_stop = Event()
    thread = Thread(target=gp_thread, args=(thread_stop, lambda_, training_data, best_individuals), daemon=True)
    thread.start()
    time.sleep(time_budget)
    thread_stop.set()
    thread.join(2)
    best_ind = best_individuals[-1]
    print(f'RAN FOR {time.time() - start_time} seconds', file=sys.stderr)
    return best_ind


def main():
    print('main', file=sys.stderr)
    args = arg_parser.parse()
    print('Question:\n{}\n'.format(args.question), file=sys.stderr)
    print('Expr:\n{}\n'.format(args.expr), file=sys.stderr)
    print('N:\n{}\n'.format(args.n), file=sys.stderr)
    print('X:\n{}\n'.format(args.x), file=sys.stderr)

    if args.question == 1:
        print('question 1:\n', file=sys.stderr)
        print(question1(args.expr, args.x))
    elif args.question == 2:
        print('question 2', file=sys.stderr)
        print(question2(args.expr, args.data))
    elif args.question == 3:
        print('question 3', file=sys.stderr)
        best_ind = question3(args.lambda_, args.data, args.time_budget)
        print('BEST IND:', file=sys.stderr)
        print(best_ind)
        print(f'FITNESS: {best_ind.fitness}', file=sys.stderr)
    else:
        print('Error: Invalid question number supplied', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
