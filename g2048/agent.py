import collections
from rich.text import Text
from rich.console import Console
import itertools

import game
import copy
import sys
import random


class Agent2048:
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    MOVES = [UP, DOWN, LEFT, RIGHT]

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
                grid_move.gen_tile_position_dict()
                # print(grid_move.tile2positions)
                lst.append(grid_move)
        return lst

    def heuristic_move(self, grid):
        self.grid = game.Grid2048(grid)
        simulations = self.gen_simulation_lst()
        lst = sorted(simulations, key=self.move_selection_priority)
        console = Console()
        self.grid.print_grid()
        for sim in lst:
            ll = sim.tile_position_analysis()
            t0 = Text('max dist: ' + str(ll[0]) + ' ' , style='red')
            t1 = Text(str(sim), style='green')
            t0.append(t1)
            console.print(t0)

        return lst[0].move

    def move_selection_priority(self, grid_obj):
        lst = grid_obj.tile_position_analysis()
        return lst[0], -grid_obj.merge_score, -grid_obj.merge_number, -grid_obj.zero_cells
