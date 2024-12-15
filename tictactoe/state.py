import string


class State:
    def __init__(self):
        self.board = string.digits[:-1]

    def whos_turn(self):
        if self.board.count('X') % 2 == 0:
            return 'X'
        else:
            return 'O'

    def get_free_cells(self) -> List[str]:
        return filter(lambda c: c != 'X' and c != 'O', self.board)

    def is_valid_move(self, cell: int) -> bool:
        return str(cell) in self.get_free_cells()

    def execute_move(self, cell, player):
        self.board = self.board.replace(self.board[cell], player)

    @property
    def winner(self):
        # check rows
        for i in range(3):
            row = self.board[i*3:i*3+3]
            if row == 'XXX':
                return 'X'
            if row == 'OOO':
                return 'O'
        # check cols
        for j in range(3):
            col = self.board[j::3]
            if col == 'XXX':
                return 'X'
            if col == 'OOO':
                return 'O'
        # check diags
        if self.board[0::4] == 'XXX' or self.board[2::2][:-1] == 'XXX':
            return 'X'
        if self.board[0::4] == 'OOO' or self.board[2::2][:-1] == 'OOO':
            return 'O'
        return None

    @property
    def is_game_over(self):
        if self.winner is None:
            return len(list(self.get_free_cells())) == 0
        else:
            return True

    def pretty_print(self):
        line = 5 * '-'
        b0 = '|'.join(self.board[0:3]) + '\n' + line
        b1 = '|'.join(self.board[3:6]) + '\n' + line
        b2 = '|'.join(self.board[6:9]) + '\n' + line
        print('\n'.join([b0, b1, b2]))
