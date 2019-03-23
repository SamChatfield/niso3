import argparse
import sys
from pathlib import Path


def _x(x_str):
    return tuple(map(float, x_str.split(' ')))


def _data(data_path_str):
    data_path = Path(data_path_str).expanduser().resolve()
    if not data_path.is_file():
        raise argparse.ArgumentTypeError(f'Data file not found at path {data_path}')
    else:
        return data_path


def parse():
    print('Parse args', file=sys.stderr)
    parser = argparse.ArgumentParser(
        description='NISO Exercise 3'
    )
    parser.add_argument(
        '-question',
        type=int,
        required=True
    )
    parser.add_argument(
        '-expr',
        type=str
    )
    parser.add_argument(
        '-n',
        type=int
    )
    parser.add_argument(
        '-x',
        type=_x
    )
    parser.add_argument(
        '-m',
        type=int
    )
    parser.add_argument(
        '-data',
        type=_data
    )
    parser.add_argument(
        '-lambda',
        type=int,
        dest='lambda_'
    )
    parser.add_argument(
        '-time_budget',
        type=int
    )
    return parser.parse_args()
