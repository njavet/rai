import random
import sys
from rich.text import Text
from pathlib import Path
from rich.console import Console
import argparse

# project imports
from rai.utils.models import Params
from rai.rl.agents.t3_agent import T3Agent
from rai.rl.envs.t3_env import T3Env


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='training mode (default: False)', action='store_const', const=True, default=False)
    parser.add_argument('-n', help='number of games in self play', default=10000)
    parser.add_argument('-m', help='model file', default='model.json')
    return parser.parse_args(argv)


def get_default_params():
    params = Params(total_episodes=2**14,
                    alpha=0.1,
                    gamma=0.99,
                    epsilon=0.8,
                    epsilon_min=0.05,
                    decay=0.99,
                    map_size=6,
                    seed=0x101,
                    is_slippery=True,
                    n_runs=64,
                    action_size=None,
                    state_size=None,
                    proba_frozen=0.75,
                    savefig_folder=Path('rl', 'figs'))
    return params


def main():
    args = parse_args(sys.argv[1:])
    training_mode = args.t
    console = Console()
    random.seed()

    console.print('Welcome to the Tic-Tac-Toe self-play RL agent environment.')
    print_help(console)

    env = T3Env()
    params = get_default_params()
    agent = T3Agent(env, params)

    # train a RL agent by self-play
    if training_mode:
        agent.run_env()

    # apply a trained RL agent in a game against a human
    else: 
        board = env.state
        try:
            model = agent.load_model()
        except FileNotFoundError:
            print('There is no model...')
            model = {}

        print('You are player O, the computer starts.')
        
        while not env.game_over:
            turn = env.whos_turn()
            agent.actions = env.available_moves()
            # X -> agent
            if turn == 1:
                state = agent.encode_state(board)
                action = agent.policy(state)
                env.step(action)
            else:
                # get player's input (until valid) and make the respective move
                valid = True
                while not valid:
                    field = input("Which field to set? ")
                    action = int(field)
                    if action not in env.available_moves():
                        valid = False
                    else:
                        env.state[action] = 2

            # print new state, evaluate game
            print('Game after ' + turn + "'s move: ")
            env.pprint_board()

        print('The game is over. ' + env.winner + ' won.')


def print_help(console=None):
    """
    Print a help text for a potential user as how to address fields in the
    board.
    """
    if console is None:
        console = Console()

    console.print("The fields in the board are addressed with "
                  "single numbers in the following way:")
    console.print('0|1|2')
    console.print('-----')
    console.print('3|4|5')
    console.print('-----')
    console.print('6|7|8')


if __name__ == '__main__':
    main()
