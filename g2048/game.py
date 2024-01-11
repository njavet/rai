from rich.text import Text
from rich.console import Console
import copy
import collections
import itertools
import functools


class Grid2048:
    """
    this grid object should be created every move
    """
    def __init__(self, grid, move=None):
        self.grid = copy.deepcopy(grid)
        self.move = move
        self.console = Console()
        self.merge_score = 0
        self.merge_number = 0
        self.zero_cells = 0
        self.tile2positions = None
        self.dmax = 0
        self.distance = None

    def __str__(self):
        s = ' '.join([str(k) + ' ' + str(v) for k, v in self.distance.items()])
        return ' '.join(['d: ', s,
                         's: ' + str(self.merge_score),
                         'm: ' + str(self.merge_number),
                         'z: ' + str(self.zero_cells)])

    def print_grid(self):
        for row in self.grid:
            self.console.print('|', end=' ')
            for val in row:
                self.console.print(str(val).rjust(4), end=' | ')
            self.console.print('\n' + 32*'-')

    def is_equal(self, grid):
        return self.grid == grid.grid

    def execute_analysis(self):
        self.gen_tile_position_dict()
        self.tile_position_analysis()
        self.max_element_upper_left()

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

    def tile_position_analysis(self):
        # remove zero since it means empty cells
        # the max value is kept here, to maybe avoid the expected
        # stupid behavior in the TODO comment
        self.tile2positions.pop(0, None)

        self.distance = {}
        for tile, positions in self.tile2positions.items():
            # there is only one tile with this number
            # distance to left upper corner
            # TODO seperate max values from others
            # TODO compare only equal values between stats
            # -> sort prioritize 2 512, over 1 1024
            # (-1, -1024, 0), (-2, -128, 2), ...
            # (-1, -1024, 0), (-1, -256, 2), ....

            # (-1, -1024, 0), (0, -256, 0), (-2, -128, 2), ...
            # (-1, -1024, 0), (-1, -256, 2), (0, -128, 0) ....

            if len(positions) == 1:
                i, j = positions[0]
                self.distance[tile] = (-1, i + j)
            # we have two tiles and want them to be close together
            elif len(positions) == 2:
                i0, j0 = positions[0]
                i1, j1 = positions[1]
                d = abs(i0 - i1) + abs(j0 - j1)
                self.distance[tile] = (-2, d)
            else:
                i0, j0 = positions[0]
                i1, j1 = positions[1]
                d = abs(i0 - i1) + abs(j0 - j1)
                self.distance[tile] = (-len(positions), d)

    def max_element_upper_left(self):
        tiles = list(self.tile2positions.keys())
        max_tile = tiles[0]
        # main priority is to keep it at the upper left
        # TODO expected "stupid" behavior if we have more than
        #  one max and the agent could merge them without risking
        #  the upper left corner position
        self.dmax = sum(self.tile2positions[max_tile][0])

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
