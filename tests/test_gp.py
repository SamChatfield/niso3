from pathlib import Path

from gp import GP
from main import parse_data


POP_SIZE = 20


def test_gp_mut(generations=20):
    data_path = Path('./containerfs/tmp/cetdl1772small.dat')
    training_data = parse_data(data_path)

    gpobj = GP(POP_SIZE, training_data, mutation_method='branch_replacement')
    gpobj.run(generations)
    # for i in range(generations):
    #     print(f'GEN {i}')
    #     gpobj.generation()
    #     print(f'FITNESSES: {sorted([i.fitness for i in gpobj._population])}')
    #     print(f'LENGTHS: {sorted([len(i.expression) for i in gpobj._population])}')
