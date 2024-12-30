import random
import numpy as np

from rai.g2048.expectimax import expectimax, simulate_move


def find_best_move(grid):
    result = [score_top_level_move(i, grid) for i in range(4)]

    if max(result) == 0:
        move = random.choice([0, 1, 2, 3])
    else:
        move = result.index(max(result))
    return move


def score_top_level_move(move, grid, depth=4):
    new_grid, _ = simulate_move(grid, move)
    if np.equal(new_grid, grid).all():
        return 0

    return expectimax(new_grid, depth, agent_play=False)
