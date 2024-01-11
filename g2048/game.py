from rich.text import Text
import copy
from rich.console import Console
import itertools
import functools


class Grid2048:
    """
    this grid object should be created every move
    """
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.merge_score = 0

    def print_grid(self):
        for row in self.grid:
            print('|', end=' ')
            for val in row:
                print(str(val).rjust(2), end=' | ')
            print('\n' + 21*'-')

    def is_equal(self, grid):
        return self.grid == grid

    def merge_seq_to_left(self, seq, acc):
        if not seq:
            return acc

        x = seq[0]
        if len(seq) == 1:
            return acc + [x]

        if x == seq[1]:
            self.merge_score += x
            return self.merge_seq_to_left(seq[2:], acc + [2 * x])
        else:
            return self.merge_seq_to_left(seq[1:], acc + [x])

    def merge_left(self):
        for i, row in enumerate(self.grid):
            merged = self.merge_seq_to_left([x for x in row if x != 0], [])
            merged_zeros = merged + (len(row) - len(merged)) * [0]
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
