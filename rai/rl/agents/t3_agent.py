import random
import numpy as np

# project imports
from rai.rl.life import Life


class T3Agent(Life):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.q_table = {}
        # TODO action space is mutable
        self.actions = None

    def decode_state(self, state):
        base = 3
        # TODO generalize
        num_cells = 9
        board_size = 3
        board = np.zeros(num_cells, dtype=np.int8)

        for i in range(num_cells - 1, -1, -1):
            board[i] = state % base
            state //= base
        return board.reshape((board_size, board_size))

    def policy(self, state: int) -> int:
        board = self.decode_state(state)
