import random
import numpy as np

# project imports
from rai.g2048.expectimax import expectimax
from rai.utils.helpers import random_argmax


class Agent:
    def __init__(self, depth: int = 3) -> None:
        self.depth = depth
        self.state = None

    def find_best_move(self, board: list[list[int]]) -> int:
        self.state = np.array(board, dtype=np.int16)
        result = np.array([self.score_top_level_move(i) for i in range(4)])

        if np.max(result) == 0:
            move = random.choice([0, 1, 2, 3])
        else:
            move = random_argmax(result)
        return move

    def score_top_level_move(self, move):
        new_grid, _ = simulate_move(self.state, move)
        if np.all(new_grid == self.state):
            return 0

        return expectimax(new_grid, self.depth, agent_play=False)


class Simulator:
    def __init__(self, state):
        self.state = state
        self.new_state = None
        self.reward = 0

    def simulate_move(self, move: int):
        if move == 0:
            self.merge_left()
        elif move == 1:
            self.merge_down()
        elif move == 2:
            self.merge_right()
        elif move == 3:
            self.merge_up()

    def merge_left(self):

        def merge_seq_to_left(seq, acc, seq_r: float = 0) -> tuple[list[int], float]:
            if not seq:
                return acc, seq_r

            x = seq[0]
            if len(seq) == 1:
                return acc + [x], seq_r

            if x == seq[1]:
                return merge_seq_to_left(seq[2:], acc + [2 * x], seq_r + 2 * x)
            else:
                return merge_seq_to_left(seq[1:], acc + [x], seq_r)

        new_grid = []
        reward = 0
        for i, row in enumerate(self.state):
            merged, r = merge_seq_to_left([x for x in row if x != 0], [])
            zeros = len(row) - len(merged)
            merged_zeros = merged + zeros * [0]
            new_grid.append(merged_zeros)
            reward += r
        self.new_state = np.array(new_grid, dtype=np.int16)
        self.reward = reward

    def merge_right(self):
        self.state = self.state[:, ::-1]
        self.merge_left()
        self.new_state = self.new_state[:, ::-1]

    def merge_up(self):
        self.state = self.state.transpose()
        self.merge_left()
        self.new_state = self.new_state.transpose()

    def merge_down(self):
        self.state = self.state.transpose()
        self.merge_right()
        self.new_state = self.new_state.transpose()
