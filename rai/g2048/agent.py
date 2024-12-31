import random
import numpy as np

# project imports
from rai.g2048.expectimax import expectimax, simulate_move
from rai.utils.helpers import random_argmax


class Agent:
    def __init__(self, depth: int = 3) -> None:
        self.depth = depth

    def find_best_move(self, board: list[list[int]]) -> int:
        grid = np.array(board, dtype=np.int16)
        result = np.array([self.score_top_level_move(i, grid) for i in range(4)])

        if np.max(result) == 0:
            move = random.choice([0, 1, 2, 3])
        else:
            move = random_argmax(result)
        return move

    def score_top_level_move(self, move, grid):
        new_grid, _ = simulate_move(grid, move)
        if np.all(new_grid == grid):
            return 0

        return expectimax(new_grid, self.depth, agent_play=False)
