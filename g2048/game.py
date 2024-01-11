from rich.text import Text
import copy
import collections
from rich.console import Console
import itertools
import functools


class Grid2048:
    """
    this grid object should be created every move
    """
    def __init__(self, grid, move=None):
        self.grid = copy.deepcopy(grid)
        self.move = move
        self.merge_score = 0
        self.merge_number = 0
        self.zero_cells = 0
        self.tile2positions = None

    def print_grid(self):
        for row in self.grid:
            print('|', end=' ')
            for val in row:
                print(str(val).rjust(2), end=' | ')
            print('\n' + 21*'-')

    def is_equal(self, grid):
        return self.grid == grid.grid

    def gen_tile_position_dict(self):
        """
        creates a SORTED dict, in a decreasing tile order
        the position lists are sored increasingly
        :return:
        """
        dix = collections.defaultdict(list)
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                dix[val].append((i, j))
        self.tile2positions = {val: sorted(dix[val])
                               for val in sorted(dix, reverse=True)}

    def merge_seq_to_left(self, seq, acc):
        if not seq:
            return acc

        x = seq[0]
        if len(seq) == 1:
            return acc + [x]

        if x == seq[1]:
            # here is the (only !) point where tiles get merged
            # therefore we compute relevant values -> ugly from
            # a functional programming viewpoint
            self.merge_score += x
            self.merge_number += 1
            return self.merge_seq_to_left(seq[2:], acc + [2 * x])
        else:
            return self.merge_seq_to_left(seq[1:], acc + [x])

    def merge_left(self):
        for i, row in enumerate(self.grid):
            merged = self.merge_seq_to_left([x for x in row if x != 0], [])
            # since `merged` has no zeros, the number of zeros can be added here
            # only here the zeros are "added" to the new grid
            zeros = len(row) - len(merged)
            self.zero_cells += zeros
            merged_zeros = merged + zeros * [0]
            self.grid[i] = merged_zeros

    def merge_right(self):
        self.grid = [row[::-1] for row in self.grid]
        self.merge_left()
        self.grid = [row[::-1] for row in self.grid]

    def merge_up(self):
        self.grid = list(zip(*self.grid))
        self.merge_left()
        self.grid = [list(x) for x in zip(*self.grid)]

    def merge_down(self):
        self.grid = list(zip(*self.grid))
        self.merge_right()
        self.grid = [list(x) for x in zip(*self.grid)]
