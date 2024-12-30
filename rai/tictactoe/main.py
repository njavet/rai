import random
import sys
from rich.text import Text
from rich.console import Console
import argparse

import t3_agent as agent
import t3_engine as engine


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='training mode (default: False)', action='store_const', const=True, default=False)
    parser.add_argument('-n', help='number of games in self play', default=10000)
    parser.add_argument('-m', help='model file', default='model.json')
    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    training_mode = args.t
    console = Console()
    random.seed()

    console.print('Welcome to the Tic-Tac-Toe self-play RL agent environment.')
    engine.print_help(console)

    # train a RL agent by self-play
    if training_mode:
        agent.train_model(args.n, args.m)
            
    # apply a trained RL agent in a game against a human
    else: 
        board = engine.get_initial_board()
        try:
            model = agent.load_model(args.m)
        except FileNotFoundError:
            print('There is no model...')
            model = {}

        print('You are player O, the computer starts.')
        
        while True:
            turn = engine.whos_turn(board)
            if turn == 'X':
                #field = agent.get_best_action(board, model, turn, debug=True)
                #field = agent.get_minimax_action(board)
                field = agent.get_expectimax_action(board)
                board = engine.make_move(board, field, turn)
                assert(board != '')
            else:
                # get player's input (until valid) and make the respective move
                while True: 
                    field = input("Which field to set? ")
                    board0 = engine.make_move(board, field, turn)
                    if board0 != '':
                        board = board0
                        break
            
            # print new state, evaluate game
            print('Game after ' + turn + "'s move: ")
            engine.print_board(board, console, False)
            game_over, who_won, reward = engine.evaluate(board)
            
            if game_over:
                print('The game is over. ' + who_won + ' won.')
                break


if __name__ == '__main__':
    main()
