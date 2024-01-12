import collections
from rich.text import Text
from rich.console import Console
import itertools
import math
import numpy as np
import functools
import operator

import game
import copy
import sys
import random


# heuristics from stackover flow post:
# bonus for zero cells
# large tiles on the edge
# penalty for non mononic rows / cols with increasing ranks
# number of potential merges (adjacent equal values) in addition
# to zero cells -> this increases delayed merges

# CMA-ES adjust weights -> maybe RL ?

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def find_best_move(grid):
    result = [score_top_level_move(i, grid) for i in range(4)]
    game.print_grid(grid)
    print('result', result)
    if max(result) == 0:
        move = random.choice([0, 1, 2, 3])
    else:
        move = result.index(max(result))
    return move


def score_top_level_move(move, grid, depth=5):
    new_grid = game.simulate_move(move, grid)
    if new_grid == grid:
        return 0
    return expectimax(new_grid, depth, agent_play=False)


class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.func(*args)
        return self.memo[args]


class GridMemo:
    def __init__(self, func):
        self.func = func
        self.memo = {}

    def __call__(self, *args, **kwargs):
        if args not in self.memo:
            self.memo[args] = self.func(*args)
        return self.memo[args]


@Memoize
def score_seq(seq):
    #print('seq', seq)
    zeros = seq.count(0)
    rank = max(seq)
    try:
        rw = 1 / rank
    except ZeroDivisionError:
        rw = 1

    ind = seq.index(rank)
    if ind == 0 or ind == 3:
        edge = 1 - rw
    else:
        edge = 0

    vals = [val for val in seq if val != 0]
    if vals == sorted(vals) or vals == sorted(vals, reverse=True):
        mono = 1 - rw
    else:
        mono = 0

    adj = 0
    for i, val in enumerate(vals[:-1]):
        if val == vals[i + 1]:
            adj += 1 - (1/val)

    #print('zeros', zeros)
    #print('edge', edge)
    #print('mono', mono)
    #print('adj', adj)
    #print('rw', rw)
    return zeros + edge + mono + adj - rw


@GridMemo
def score_function(grid):
    score = 0
    for row in grid:
        score += score_seq(row)
    for col in zip(*grid):
        score += score_seq(col)
    return score


def expectimax(grid, depth, agent_play):
    if depth == 0:
        return score_function(tuple(tuple(row) for row in grid))

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

