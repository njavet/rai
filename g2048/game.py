from rich.text import Text
from rich.console import Console
import itertools
import functools


def merge_left(grid):

    def merge_seq(seq, acc):
        if not seq:
            return acc

        x = seq[0]
        if len(seq) == 1:
            return acc + [x]

        if x == seq[1]:
            return merge_seq(seq[2:], acc + [2 * x])
        else:
            return merge_seq(seq[1:], acc + [x])

    merged_grid = []
    for i, row in enumerate(grid):
        merged = merge_seq([x for x in row if x != 0], [])
        merged_zeros = merged + (len(row) - len(merged)) * [0]
        merged_grid.append(merged_zeros)
    return merged_grid


def merge_right(grid):
    t = [row[::-1] for row in grid]
    return [row[::-1] for row in merge_left(t)]


def merge_up(grid):
    t = merge_left(zip(*grid))
    return [list(x) for x in zip(*t)]


def merge_down(grid):
    t = merge_right(zip(*grid))
    return [list(x) for x in zip(*t)]


def move_exists(grid):
    if grid != merge_left(grid):
        return True
    if grid != merge_right(grid):
        return True
    if grid != merge_up(grid):
        return True
    if grid != merge_down(grid):
        return True

    return False


def equal_grids(grid0, grid1):
    return grid0 == grid1


def get_max_value(grid):
    mv, i = max(max((row, i) for i, row in enumerate(grid)))
    return i, mv[i].index(mv), mv


def print_board(grid):
    for row in grid:
        print('|', end=' ')
        for val in row:
            print(str(val).rjust(2), end=' | ')
        print('\n' + 21*'-')


