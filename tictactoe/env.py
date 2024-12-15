from rich.console import Console


class Env:
    def __init__(self):
        self.board = 9 * ' '


class State:
    def __init__(self):
        pass


class Reward:
    def __init__(self):
        pass


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

