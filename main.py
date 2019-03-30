import csv
import logging
import queue
import sys
import time
from threading import Event, Thread

import arg_parser
import gp
from expression import Expression
from individual import Individual

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.WARNING)


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
        i += 1


def question3(lambda_, data, time_budget):
    training_data = parse_data(data)
    return gp.run_gp(time_budget, lambda_, training_data)


def main():
    args = arg_parser.parse()

    if args.debug:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    logging.debug('Question: %s', args.question)

    if args.question == 1:
        logging.debug('question 1:')
        print(question1(args.expr, args.x))
    elif args.question == 2:
        logging.debug('question 2')
        print(question2(args.expr, args.data))
    elif args.question == 3:
        logging.debug('question 3')
        best_ind = question3(args.lambda_, args.data, args.time_budget)
        logging.debug('BEST IND:')
        print(best_ind)
        logging.debug('FITNESS: %s', best_ind.fitness)
    else:
        logging.error('Invalid question number supplied')
        sys.exit(1)


if __name__ == '__main__':
    main()
