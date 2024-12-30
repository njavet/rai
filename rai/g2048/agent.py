import random

from rai.g2048.expectimax import expectimax, simulate_move


def find_best_move(grid):
    result = [score_top_level_move(i, grid) for i in range(4)]
    print('result', result)

    if max(result) == 0:
        move = random.choice([0, 1, 2, 3])
    else:
        move = result.index(max(result))
    return move


def score_top_level_move(move, grid, depth=4):
    new_grid = simulate_move(grid, move)
    if new_grid == grid:
        return 0

    return expectimax(new_grid, depth, agent_play=False)
