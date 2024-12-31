import random
import numpy as np

# project imports
from rai.rl.life import Life


class T3Agent(Life):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.vtable = {}
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

    def encode_state(self, state) -> int:
        tern = np.array([3**(9 - i) for i in range(1, 9 + 1)])
        return int(np.sum(state * tern))

    def policy(self, state: int) -> int:
        board = self.decode_state(state)
        epsilon = max(self.params.epsilon_min, self.params.epsilon * self.params.decay)
        if np.random.rand() < epsilon:
            return np.random.choice(self.actions)

        acts = []
        for action in self.actions:
            sim_board = np.copy(board)
            sim_board[action] = 1
            sim_state = self.encode_state(sim_board)
            val = self.vtable.get(sim_state, 0.5)
            acts.append((val, action))
        return sorted(acts, reverse=True)[0][1]

    def process_step(self, next_state):
        # Compute the temporal difference (TD) target
        ts = self.trajectory.steps[-1]
        state, action, reward = ts.state, ts.action, ts.reward
        next_val = self.vtable.get(next_state, 0.5)
        tmp = reward + self.params.gamme * next_val - self.vtable[state]
        self.vtable[state] += self.params.alpha * tmp
