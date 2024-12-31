from rich.console import Console
from rich.text import Text

# project imports
from rai.rl.envs.base import BaseEnv, ObservationSpace, ActionSpace


class T3Env(BaseEnv):
    def __init__(self):
        super().__init__('tictactoe')
        self.console = Console()
        self.winner = None

    @property
    def game_over(self):
        if self.winner:
            return True
        free_cells = self.state.get_free_cells()
        if not free_cells:
            return True

        return False

    def is_valid_action(self, action):
        free_cells = self.state.get_free_cells()
        if action in free_cells:
            return True
        else:
            return False

    def execute_action(self, action, sym):
        old_board = self.state.board
        new_board = old_board[0:action] + sym + old_board[action+1:]
        self.state.board = new_board
        return self.state

    def pprint_board(self):
        """
        Pretty-prints the BOARD in the way described above (Description of the game
        state). If IF_NUMBERS == True, the emtpy fields are printed with their
        respective field numbers.
        """
        hl = 13 * '-'
        r0 = ' | '.join(self.env.state.board[0:3])
        r1 = ' | '.join(self.env.state.board[3:6])
        r2 = ' | '.join(self.env.state.board[6:9])

        self.console.print(hl, style='#6312ff')
        self.console.print('| ' + r0 + ' |', style='cyan')
        self.console.print(hl, style='#6312ff')
        self.console.print('| ' + r1 + ' |', style='cyan')
        self.console.print(hl, style='#6312ff')
        self.console.print('| ' + r2 + ' |', style='cyan')
        self.console.print(hl, style='#6312ff')

        if with_numbers:
            # replace ' ' by field-number
            board = ''.join([str(i) if board[i] == ' ' else board[i] for i in range(9)])

        t0 = Text('|'.join([*board[0:3]]) + '\n-----\n')
        t1 = Text('|'.join([*board[3:6]]) + '\n-----\n')
        t2 = Text('|'.join([*board[6:9]]))
        console.print('\n-----\n'.join([
            '|'.join([*board[0:3]]),
            '|'.join([*board[3:6]]),
            '|'.join([*board[6:9]])
        ]))


class ObsSpace(ObservationSpace):
    def __init__(self):
        super().__init__(size=9, start=None, terminal=None)

    def get_free_cells(self):
        free_cells = []
        for i, cell in enumerate(self.board):
            if cell == ' ':
                free_cells.append(i)
        return free_cells

    def get_winner(self):
        # check rows
        rows = [self.board[0:3], self.board[3:6], self.board[6:]]
        if any([row == 'XXX' for row in rows]):
            return 'X'
        elif any([row == 'OOO' for row in rows]):
            return 'O'
        # check columns
        cols = [self.board[0::3], self.board[1::3], self.board[2::3]]
        if any([col == 'XXX' for col in cols]):
            return 'X'
        elif any([col == 'OOO' for col in cols]):
            return 'O'

        if self.board[0::4] == 'OOO':
            return 'O'
        elif self.board[0::4] == 'XXX':
            return 'X'

        if self.board[2::2] == 'OOO':
            return 'O'
        elif self.board[2::2] == 'XXX':
            return 'X'



def evaluate(board):

    # check rows
    rows = [board[0:3], board[3:6], board[6:9]]
    if any(r == 'XXX' for r in rows):
        return True, 'X', 1
    elif any(r == 'OOO' for r in rows):
        return True, 'O', -1

    # check cols
    cols = [board[::3], board[1::3], board[2::3]]
    if any(c == 'XXX' for c in cols):
        return True, 'X', 1
    elif any(c == 'OOO' for c in cols):
        return True, 'O', -1

    # check diags
    diags = [board[::4], board[2:-1:2]]
    if any(d == 'XXX' for d in diags):
        return True, 'X', 1
    elif any(d == 'OOO' for d in diags):
        return True, 'O', -1

    # check draw (board full):
    if count_symbol(board, ' ') == 0:
        return True, 'Nobody', 0

    # otherwise: game not over
    return False, 'Nobody', 0

