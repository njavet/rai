from rich.console import Console
import numpy as np
from rich.text import Text

# project imports
from rai.rl.envs.base import BaseEnv


class T3Env(BaseEnv):
    def __init__(self):
        super().__init__('tictactoe')
        self.console = Console()
        self.size = 9
        self.state = np.zeros(self.size, dtype=np.int8)
        self.winner = None

    def reset(self) -> tuple[int, str]:
        self.state = np.zeros(9, dtype=np.int8)
        return 0, 'reset'

    # TODO different than other envs, move restrictions
    def available_moves(self) -> list[int]:
        return [int(a) for a in np.where(self.state == 0)[0]]

    def whos_turn(self):
        if np.where(self.state == 0)[0].size % 2 == 0:
            player = 2
        else:
            player = 1
        return player

    def step(self, action):
        if np.where(self.state == 0)[0].size % 2 == 0:
            player = 2
            actions = self.available_moves()
            action = np.random.choice(actions)
        else:
            player = 1
        self.state[action] = player
        self.determine_winner()
        if self.winner == 1:
            term = True
            reward = 1
        elif self.winner == 2:
            term = True
            reward = -1
        elif self.game_over:
            term = True
            reward = 0
        else:
            term = False
            reward = 0
        return self.encode_state(), reward, term, False, None

    def encode_state(self) -> int:
        tern = np.array([3**(self.size - i) for i in range(1, self.size + 1)])
        return int(np.sum(self.state * tern))

    def determine_winner(self):
        board = [int(a) for a in self.state]
        winning = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
                self.winner = board[combo[0]]
                break
            else:
                self.winner = None

    @property
    def game_over(self):
        if self.winner:
            return True
        elif np.sum(np.where(self.state == 0)) == 0:
            return True
        else:
            return False

    def pprint_board(self):
        """
        Pretty-prints the BOARD in the way described above (Description of the game
        state). If IF_NUMBERS == True, the emtpy fields are printed with their
        respective field numbers.
        """
        dix = {0: ' ',
               1: 'X',
               2: 'O'}

        hl = 13 * '-'
        r0 = ' | '.join(map(lambda x: dix[x], self.state[0:3]))
        r1 = ' | '.join(map(lambda x: dix[x], self.state[3:6]))
        r2 = ' | '.join(map(lambda x: dix[x], self.state[6:9]))

        self.console.print(hl, style='#6312ff')
        self.console.print('| ' + r0 + ' |', style='cyan')
        self.console.print(hl, style='#6312ff')
        self.console.print('| ' + r1 + ' |', style='cyan')
        self.console.print(hl, style='#6312ff')
        self.console.print('| ' + r2 + ' |', style='cyan')
        self.console.print(hl, style='#6312ff')
