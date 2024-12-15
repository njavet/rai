from rich.console import Console


class Env:
    def __init__(self):
        self.board = 9 * ' '
        self.state = State(self.board)
        self.reward = Reward(self.board)
        self.winner = None

    @property
    def game_over(self):
        self.winner = self.get_winner()
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

    def get_winner(self):
        # check rows
        rows = [self.state[0:3], self.state[3:6], self.state[6:]]
        if any([row == 'XXX' for row in rows]):
            return 'X'
        elif any([row == 'OOO' for row in rows]):
            return 'O'
        # check columns
        cols = [self.state[0::3], self.state[1::3], self.state[2::3]]
        if any([col == 'XXX' for col in cols]):
            return 'X'
        elif any([col == 'OOO' for col in cols]):
            return 'O'

        if self.state[0::4] == 'OOO':
            return 'O'
        elif self.state[0::4] == 'XXX':
            return 'X'

        if self.state[2::2] == 'OOO':
            return 'O'
        elif self.state[2::2] == 'XXX':
            return 'X'

    def execute_action(self, action, sym):
        self.board = self.board[0:action] + sym + self.board[action+1:]
        self.state.update_state(self.board)


class State:
    def __init__(self, board):
        self.board = board

    def is_init(self):
        return self.board == 9 * ' '

    def get_free_cells(self):
        free_cells = []
        for i, cell in enumerate(self.board):
            if cell == ' ':
                free_cells.append(i)
        return free_cells

    def update_state(self, board):
        self.board = board


class Reward:
    def __init__(self, board):
        self.board = board


class EnvPres:
    def __init__(self, env):
        self.env = env
        self.console = Console()

    def pprint_board(self):
        hl = 13 * '-'
        r0 = ' | '.join(self.env.board[0:3])
        r1 = ' | '.join(self.env.board[3:6])
        r2 = ' | '.join(self.env.board[6:9])

        self.console.print(hl, style='#6312ff')
        self.console.print('| ' + r0 + ' |', style='cyan')
        self.console.print(hl, style='#6312ff')
        self.console.print('| ' + r1 + ' |', style='cyan')
        self.console.print(hl, style='#6312ff')
        self.console.print('| ' + r2 + ' |', style='cyan')
        self.console.print(hl, style='#6312ff')

