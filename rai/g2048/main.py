import time
import argparse


# project imports
from rai.rl.rl2048.ffctrl import FirefoxRemoteControl
from rai.rl.rl2048.chromectrl import ChromeDebuggerControl
from rai.rl.rl2048.gamectrl import (Fast2048Control,
                                    Keyboard2048Control,
                                    Hybrid2048Control)
import rai.rl.rl2048.heuristicai as ai


def print_board(m):
    for row in m:
        for c in row:
            print('%8d' % c, end=' ')
        print()

def _to_val(c):
    if c == 0: return 0
    return c

def to_val(m):
    return [[_to_val(c) for c in row] for row in m]

def _to_score(c):
    if c <= 1:
        return 0
    return (c-1) * (2**c)

def to_score(m):
    return [[_to_score(c) for c in row] for row in m]

def find_best_move(board):
    return ai.find_best_move(board)

def movename(move):
    return ['up', 'down', 'left', 'right'][move]

def play_game(gamectrl):
    moveno = 0
    start = time.time()
    while 1:
        state = gamectrl.get_status()
        if state == 'ended':
            break
        elif state == 'won':
            time.sleep(0.75)
            gamectrl.continue_game()

        moveno += 1
        board = gamectrl.get_board()
        move = find_best_move(board)
        if move < 0:
            break
        print("%010.6f: Score %d, Move %d: %s" % (time.time() - start, gamectrl.get_score(), moveno, movename(move)))
        gamectrl.execute_move(move)

    score = gamectrl.get_score()
    board = gamectrl.get_board()
    maxval = max(max(row) for row in to_val(board))
    print("Game over. Final score %d; highest tile %d." % (score, maxval))


def create_parser():
    parser = argparse.ArgumentParser(
        description='Use the AI to play 2048 via browser control')
    parser.add_argument('-c', '--ctrl_mode',
                        default='hybrid',
                        dest='ctrl_mode',
                        choices=('keyboard', 'fast', 'hybrid'),
                        help='Control mode to use. If the browser control'
                             'does not seem to work, try changing this.')
    return parser


def g2048():
    parser = create_parser()
    args = parser.parse_args()

    if args.ctrl_mode == 'keyboard':
        game_ctrl = Keyboard2048Control(ctrl)
    elif args.ctrl_mode == 'fast':
        game_ctrl = Fast2048Control(ctrl)
    elif args.ctrl_mode == 'hybrid':
        game_ctrl = Hybrid2048Control(ctrl)
    else:
        raise ValueError('wrong control')

    if game_ctrl.get_status() == 'ended':
        game_ctrl.restart_game()

    play_game(game_ctrl)
