import argparse

# project imports
from state import State
from agent import Agent


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--games', type=int, default=100, dest='games')
    return parser


def play_game(game, training_mode=False):
    s = State()

    while not s.game_over:
        if s.whos_turn() == 'O':
            s.pretty_print()
            move = int(input('Enter your next move'))
            while not s.is_valid_move(move):
                move = int(input('invalid move... try again:'))
            s.execute_move(move, 'O')
            s.is_game_over()



def main():
    parser = create_parser()
    args = parser.parse_args()

    for game in args.games:
        play_game(game)


if __name__ == '__main__':
    main()
