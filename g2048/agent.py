import collections
from rich.text import Text
from rich.console import Console
import itertools
import math

import game
import copy
import sys
import random


class Agent2048:
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    MOVES = [UP, DOWN, LEFT, RIGHT]
    MOVES_NAMES = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def __init__(self):
        self.t = 0
        self.grid = None

    def random_move(self):
        return random.choice(self.MOVES)

    def simulate_move(self, move):
        grid = game.Grid2048(self.grid.grid, move)
        if move == self.UP:
            grid.merge_up()
        elif move == self.DOWN:
            grid.merge_down()
        elif move == self.LEFT:
            grid.merge_left()
        elif move == self.RIGHT:
            grid.merge_right()
        if not self.grid.is_equal(grid):
            return grid

    def gen_simulation_lst(self):
        lst = []
        for move in self.MOVES:
            grid_move = self.simulate_move(move)
            if grid_move:
                grid_move.execute_analysis()
                lst.append(grid_move)
        return lst

    def gen_tile_list(self, simulations):
        max_tile = max([list(grid_obj.tile2positions.keys())[0]
                        for grid_obj in simulations])
        vals = [max_tile]
        for e in range(int(math.log2(max_tile)), 1, -1):
            vals.append(2 ** e)
        return vals

    def heuristic_move(self, grid):
        self.grid = game.Grid2048(grid)
        simulations = self.gen_simulation_lst()
        vals = self.gen_tile_list(simulations)

        lst = sorted(simulations,
                     key=lambda el: self.move_selection_priority(el,
                                                                 vals))

        console = Console()
        self.grid.print_grid()
        for sim in lst:
            t = Text(str(sim), style='green')
            console.print(t)

        return lst[0].move

    def move_selection_priority(self, grid_obj, vals):
        p0 = grid_obj.dmax

        lst = []
        for tile in vals:
            if tile in grid_obj.distance:
                lst.append(grid_obj.distance[tile])
            else:
                lst.append((0, 0, 0, 0))

        p3 = -grid_obj.merge_number
        p4 = -grid_obj.zero_cells
        return p0, lst, p3, p4
