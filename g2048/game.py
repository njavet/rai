import random

from rich.text import Text
from rich.console import Console
import copy
import math
import collections
import itertools
import numpy as np
import functools


def merge_left(grid):
    def merge_seq_to_left(seq, acc):
        if not seq:
            return acc

        x = seq[0]
        if len(seq) == 1:
            return acc + [x]

        if x == seq[1]:
            # here is the (only !) point where tiles get merged
            # therefore we compute relevant values -> ugly from
            # a functional programming viewpoint
            return merge_seq_to_left(seq[2:], acc + [2 * x])
        else:
            return merge_seq_to_left(seq[1:], acc + [x])

    new_grid = []
    for i, row in enumerate(grid):
        merged = merge_seq_to_left([x for x in row if x != 0], [])
        # since `merged` has no zeros, the number of zeros can be added here
        # only here the zeros are "added" to the new grid
        zeros = len(row) - len(merged)
        merged_zeros = merged + zeros * [0]
        new_grid.append(merged_zeros)
    return new_grid


def merge_right(grid):
    t = merge_left(np.array([row[::-1] for row in grid]))
    #return np.array([row[::-1] for row in t])
    return [row[::-1] for row in t]


def merge_up(grid):
    #t = merge_left(grid.transpose())
    t = merge_left(zip(*grid))
    #return t.transpose()
    return [list(x) for x in zip(*t)]


def merge_down(grid):
    #t = merge_right(grid.transpose())
    t = merge_right(zip(*grid))
    #return t.transpose()
    return [list(x) for x in zip(*t)]


def simulate_move(move, grid):
    if move == 0:
        return merge_up(grid)
    elif move == 1:
        return merge_down(grid)
    elif move == 2:
        return merge_left(grid)
    elif move == 3:
        return merge_right(grid)


def move_available(grid):
    mg = merge_up(grid)
    if mg != grid:
        return True
    mg = merge_down(grid)
    if mg != grid:
        return True
    mg = merge_left(grid)
    if mg != grid:
        return True
    mg = merge_right(grid)
    if mg != grid:
        return True


def is_move_available(grid, move):
    new_grid = simulate_move(move, grid)
    return new_grid != grid


def print_grid(grid, console=None):
    if console is None:
        console = Console()
    for row in grid:
        console.print('|', end=' ')
        for val in row:
            console.print(str(val).rjust(4), end=' | ')
        console.print('\n' + 29*'-')


class Game(object):
    # actions = [up, down, left, right] -> [0, 1, 2, 3]
    def __init__(self, state=None, initial_score=0):
        self.score = initial_score
        if state is None:
            self.state = [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]
            self.add_random_tile()
            self.add_random_tile()
        else:
            self.state = state

    def copy(self):
        return Game(copy.deepcopy(self.state), self.score)

    def game_over(self):
        return not move_available(self.state)

    def available_actions(self):
        return [action for action in range(4)
                if is_move_available(self.state, action)]

    def execute_action(self, action):
        reward = 0
        # up
        if action == 0:
            reward = self.merge_up()
        # down
        if action == 1:
            reward = self.merge_down()
        # left
        if action == 2:
            reward = self.merge_left()
        # right
        if action == 3:
            reward = self.merge_right()
        self.score += reward
        self.add_random_tile()
        return reward

    def add_random_tile(self):
        inds = [(i, j) for (i, j) in itertools.product(range(4), repeat=2)
                if self.state[i][j] == 0]
        assert(len(inds) > 0)
        i, j = random.choice(inds)
        value = np.random.choice([1, 2], p=[0.9, 0.1])
        self.state[i][j] = value

    def merge_left(self):
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

        new_state = []
        reward = 0
        for i, row in enumerate(self.state):
            merged, r = merge_seq_to_left([x for x in row if x != 0], [])
            zeros = len(row) - len(merged)
            merged_zeros = merged + zeros * [0]
            new_state.append(merged_zeros)
            reward += r
        self.state = new_state
        return reward

    def merge_right(self):
        self.state = [row[::-1] for row in self.state]
        reward = self.merge_left()
        self.state = [row[::-1] for row in self.state]
        return reward

    def merge_up(self):
        self.state = zip(*self.state)
        reward = self.merge_left()
        self.state = [list(x) for x in zip(*self.state)]
        return reward

    def merge_down(self):
        self.state = zip(*self.state)
        reward = self.merge_right()
        self.state = [list(x) for x in zip(*self.state)]
        return reward
