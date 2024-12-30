import random
import numpy as np

# project imports
from rai.g2048.expectimax import expectimax, simulate_move, is_move_available
from rai.utils.helpers import random_argmax


def find_best_move(grid):
    result = np.array([score_top_level_move(i, grid) if is_move_available(grid, i)
                      else 0 for i in range(4)])
    print(result)

    if np.max(result) == 0:
        move = random.choice([0, 1, 2, 3])
    else:
        move = random_argmax(result)
    return move


def score_top_level_move(move, grid, depth=3):
    new_grid, _ = simulate_move(grid, move)
    if np.equal(new_grid, grid).all():
        return 0

    return expectimax(new_grid, depth, agent_play=False)
