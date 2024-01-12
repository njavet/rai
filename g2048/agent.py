import collections
from rich.text import Text
from rich.console import Console
import itertools
import math

import game
import copy
import sys
import random


UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def find_best_move(grid):
    result = [score_top_level_move(i, grid) for i in range(4)]
    print('result', result)
    return result.index(max(result))


def score_top_level_move(move, grid):
    new_grid = game.simulate_move(move, grid)
    if grid == new_grid:
        print('invalid move', move)
        return 0
    return expectimax(new_grid, depth=1, agent_play=False)


def expectimax(grid, depth, agent_play):
    if depth == 0:
        grid_obj = game.Grid2048(grid)
        grid_obj.execute_analysis()
        return grid_obj.score

    if agent_play:
        alpha = 0
        for move in range(4):
            new_grid = game.simulate_move(move, grid)
            if new_grid != grid:
                alpha = max(alpha, expectimax(new_grid, depth-1, False))
        return alpha
    else:
        alpha = 0
        zero_cells = [(i, j) for i, row in enumerate(grid)
                      for j, val in enumerate(row) if val == 0]
        zeros = len(zero_cells)
        try:
            p = 1 / zeros
        except ZeroDivisionError:
            print('NO free cells')
            return expectimax(grid, depth-1, True)

        for i, j in zero_cells:
            ng2 = copy.deepcopy(grid)
            ng2[i][j] = 2
            alpha += p * 0.9 * expectimax(ng2, depth-1, True)

        for i, j in zero_cells:
            ng4 = copy.deepcopy(grid)
            ng4[i][j] = 4
            alpha += p * 0.1 * expectimax(ng4, depth-1, True)
        return alpha
