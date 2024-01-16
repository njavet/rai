from rich.text import Text
from rich.console import Console

import random
import itertools
import numpy as np


def add_random_tile(grid):
    inds = [(i, j) for (i, j) in itertools.product(range(4), repeat=2)
            if grid[i][j] == 0]
    assert(len(inds) > 0)
    i, j = random.choice(inds)
    value = np.random.choice([2, 4], p=[0.9, 0.1])
    grid[i][j] = value
    return grid


def merge_left(grid):

    def merge_seq_to_left(seq, acc, seq_r=0):
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
    for i, row in enumerate(grid):
        merged, r = merge_seq_to_left([x for x in row if x != 0], [])
        zeros = len(row) - len(merged)
        merged_zeros = merged + zeros * [0]
        new_grid.append(merged_zeros)
        reward += r
    return np.array(new_grid), reward


def merge_right(grid):
    new_grid, reward = merge_left(np.array([row[::-1] for row in grid]))
    return np.array([row[::-1] for row in new_grid]), reward


def merge_up(grid):
    new_grid, reward = merge_left(grid.transpose())
    return new_grid.transpose(), reward


def merge_down(grid):
    new_grid, reward = merge_right(grid.transpose())
    return new_grid.transpose(), reward


def simulate_move(grid, move):
    if move == 0:
        return merge_up(grid)
    elif move == 1:
        return merge_down(grid)
    elif move == 2:
        return merge_left(grid)
    elif move == 3:
        return merge_right(grid)


def available_moves(grid):
    moves = []
    mg0 = merge_up(grid)
    if mg0 != grid:
        moves.append(0)
    mg1 = merge_down(grid)
    if mg1 != grid:
        moves.append(1)
    mg2 = merge_left(grid)
    if mg2 != grid:
        moves.append(2)
    mg3 = merge_right(grid)
    if mg3 != grid:
        moves.append(3)
    return moves


def is_move_available(grid, move):
    am = available_moves(grid)
    return move in am


def print_grid(grid, console=None):
    if console is None:
        console = Console()
    for row in grid:
        console.print('|', end=' ')
        for val in row:
            console.print(str(val).rjust(4), end=' | ')
        console.print('\n' + 29*'-')
