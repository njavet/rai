import collections
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
                print(grid_move.tile2positions)
                lst.append(grid_move)
        return lst

    def heuristic_move(self, grid):
        self.grid = game.Grid2048(grid)
        simulations = self.gen_simulation_lst()
        lst = sorted(simulations, key=lambda sim: (sim.merge_score,
                                                   sim.merge_number,
                                                   sim.zero_cells),
                     reverse=True)
        return lst[0].move
