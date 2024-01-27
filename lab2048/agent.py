import collections
from rich.text import Text
from rich.console import Console
import itertools
import math
import numpy as np
import functools
import operator

import copy
import sys
import random
import torch

import grid2048


UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def find_best_move(grid):
    result = [score_top_level_move(i, grid) for i in range(4)]
    print('result', result)

    if max(result) == 0:
        move = random.choice([0, 1, 2, 3])
    else:
        move = result.index(max(result))
    return move


def score_top_level_move(move, grid, depth=4):
    new_grid = grid2048.simulate_move(grid, move)
    if new_grid == grid:
        return 0

    return grid2048.expectimax(new_grid, depth, agent_play=False)

