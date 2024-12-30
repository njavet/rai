import time
import argparse


# project imports
from ffctrl import FirefoxRemoteControl
from chromectrl import ChromeDebuggerControl
from gamectrl import Fast2048Control, Keyboard2048Control, Hybrid2048Control
import heuristicai as ai


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
    parser.add_argument(
        '-p',
        '--port',
        help='Port number to control on (default: 32000 for Firefox, 9222 for Chrome)',
        type=int)
    parser.add_argument(
        '-b',
        '--browser',
        help='Browser you are using.'
             'Only Firefox with the Remote Control extension,'
             'and Chrome with remote debugging (default),'
             'are supported right now.',
        choices=('firefox', 'chrome'))
    parser.add_argument(
        '-k',
        '--ctrlmode',
        help='Control mode to use. If the browser control does not seem to work, '
             'try changing this.',
        default='hybrid',
        choices=('keyboard', 'fast', 'hybrid'))
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.browser == 'firefox':
        if args.port is None:
            args.port = 32000
        ctrl = FirefoxRemoteControl(args.port)
    elif args.browser == 'chrome':
        if args.port is None:
            args.port = 9222
        ctrl = ChromeDebuggerControl(args.port)

    if args.ctrlmode == 'keyboard':
        gamectrl = Keyboard2048Control(ctrl)
    elif args.ctrlmode == 'fast':
        gamectrl = Fast2048Control(ctrl)
    elif args.ctrlmode == 'hybrid':
        gamectrl = Hybrid2048Control(ctrl)

    if gamectrl.get_status() == 'ended':
        gamectrl.restart_game()

    play_game(gamectrl)


if __name__ == '__main__':
    main()
