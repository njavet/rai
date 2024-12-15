import argparse

# project imports
from tictactoe.env import Env, EnvPres
from tictactoe.agent import Agent


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
    agent = Agent(env.state)

    # training mode, self play
    if args.tmode:
        pass

    # play against another agent
    else:
        print('New game, agent starts...')
        agent.act()
        env_pres.pprint_board()
        while not env.game_over:
            cell = input('Your turn: ')
            while not env.is_valid_action(cell):
                cell = input('invalid move, choose again: ')
            env.execute_action(cell, 'O')
            env_pres.pprint_board()
        print('winner:', env.winner)

