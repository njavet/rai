from rich.text import Text
from rich.console import Console
import copy
import math
import collections
import itertools
import functools


class Grid2048:
    """
    this grid object should be created every move
    """
    def __init__(self, grid):
        self.console = Console()
        self.grid = copy.deepcopy(grid)
        self.zero_cells = 0
        self.rank = 0
        self.dmax = 0
        self.tile2positions = None
        self.distance = None
        self.score = 0

    def print_grid(self):
        for row in self.grid:
            self.console.print('|', end=' ')
            for val in row:
                self.console.print(str(val).rjust(4), end=' | ')
            self.console.print('\n' + 32*'-')

    def execute_analysis(self):
        self.gen_tile_position_dict()
        self.tile_position_analysis()
        self.max_element_upper_left()
        self.monotony()
        self.set_score()

    def monotony(self):
        pass

    def tile_value_score(self):
        ts = 0
        for tile, positions in self.tile2positions.items():
            base = 10 ** int(math.log2(tile))
            ts += len(positions) * base
        return ts

    def set_score(self):

        # empty spaces heuristic
        self.score = self.zero_cells
        # distance to left upper corner
        self.score -= 100000 * self.dmax
        # highest tile
        self.score += self.rank
        # total values
        self.score += self.tile_value_score()

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
        self.zero_cells = len(self.tile2positions.pop(0, []))

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
                self.distance[tile] = (1, i + j, i + j)
            # we have two tiles and want them to be close together
            elif len(positions) == 2:
                i0, j0 = positions[0]
                i1, j1 = positions[1]
                d = abs(i0 - i1) + abs(j0 - j1)
                self.distance[tile] = (2, d, i0 + i1 + j0 + j1)
            else:
                lst = []
                for (i0, j0), (i1, j1) in itertools.combinations(positions, r=2):
                    d = abs(i0 - i1) + abs(j0 - j1)
                    s = i0 + j0 + i1 + j1
                    lst.append((d, s))
                lst.sort()
                self.distance[tile] = (len(lst), lst[0][0], lst[0][1])

    def max_element_upper_left(self):
        tiles = list(self.tile2positions.keys())
        max_tile = tiles[0]
        self.rank = max_tile
        # main priority is to keep it at the upper left
        # TODO expected "stupid" behavior if we have more than
        #  one max and the agent could merge them without risking
        #  the upper left corner position
        self.dmax = sum(self.tile2positions[max_tile][0])



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
    t = merge_left([row[::-1] for row in grid])
    return [row[::-1] for row in t]


def merge_up(grid):
    t = merge_left(zip(*grid))
    return [list(x) for x in zip(*t)]


def merge_down(grid):
    t = merge_right(zip(*grid))
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
