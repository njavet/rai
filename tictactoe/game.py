import argparse

# project imports
from tictactoe.env import Env, EnvPres


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', dest='games', default=1000, type=int)
    parser.add_argument('-m', dest='tmode', default=1, type=int)
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    env = Env()
    env_pres = EnvPres(env)
    # training mode, self play
    if args.tmode:
        pass

    # play against another agent
    else:
        env_pres.pprint_board()
        pass

