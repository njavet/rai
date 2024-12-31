import random
from rich.text import Text
from pathlib import Path
from rich.console import Console
import argparse

# project imports
from rai.utils.models import Params
from rai.rl.agents.t3_agent import T3Agent
from rai.rl.envs.t3_env import T3Env


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='training mode (default: False)', type=int)
    parser.add_argument('-n', help='number of games in self play', default=10000)
    parser.add_argument('-m', help='model file', default='model.json')
    return parser


def get_default_params():
    params = Params(total_episodes=2**16,
                    alpha=0.1,
                    gamma=0.98,
                    epsilon=0.8,
                    epsilon_min=0.05,
                    decay=0.99,
                    map_size=6,
                    seed=0x101,
                    is_slippery=True,
                    n_runs=64,
                    action_size=9,
                    state_size=3,
                    proba_frozen=0.75,
                    savefig_folder=Path('rl', 'figs'))
    return params


def main():
    parser = create_parser()
    args = parser.parse_args()
    console = Console()

    console.print('Welcome to the Tic-Tac-Toe self-play RL agent environment.')
    print_help(console)

    env = T3Env()
    params = get_default_params()
    agent = T3Agent(env, params)

    # train a RL agent by self-play
    if args.t == 1:
        agent.actions = env.available_moves()
        agent.run_env()

    # apply a trained RL agent in a game against a human
    else: 
        board = env.state
        try:
            agent.load_model()
            agent.params.epsilon = 0
        except FileNotFoundError:
            print('There is no model...')

        print('You are player O, the computer starts.')
        
        while not env.game_over:
            turn = env.whos_turn()
            # X -> agent
            if turn == 1:
                agent.actions = env.available_moves()
                state = agent.encode_state(board)
                action = agent.policy(state)
                env.step(action)
            else:
                # get player's input (until valid) and make the respective move
                invalid = True
                while invalid:
                    actions = env.available_moves()
                    action = int(input('Which field to set?'))
                    if action not in actions:
                        print('invalid move')
                        print('moves:', actions)
                    else:
                        env.state[action] = 2
                        invalid = False
            env.determine_winner()
            # print new state, evaluate game
            if turn == 1:
                tt = 'X'
            else:
                tt = 'O'
            print('Game after ' + tt + "'s move: ")
            env.pprint_board()
            print('state:', env.encode_state())

        if env.winner == 1:
            tt = 'X'
        elif env.winner == 2:
            tt = 'O'
        else:
            tt = 'nobody'
        print('The game is over. ' + tt + ' won.')


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
