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

    def expectimax(self, grid, depth=2):
        """
        insane how different this looks... nothing like
        avoiding full boards. incredible to look at it

        yet the machine only achieved 11828, with the highest tile 1024


        :param grid:
        :param depth:
        :return:
        """

        def expectimax_rec(move, grid):
            score, new_grid = self.non_oo_simulate_move(move, grid)
            if new_grid == grid:
                return

            zeros = 0
            score2 = 0
            score4 = 0
            ng2 = copy.deepcopy(grid)
            ng4 = copy.deepcopy(grid)
            for i, row in enumerate(new_grid):
                for j, val in enumerate(row):
                    if val == 0:
                        zeros += 1
                        for move2 in self.MOVES:
                            ng2[i][j] = 2
                            sc2, _ = self.non_oo_simulate_move(move2, ng2)
                            score2 += 0.9 * sc2

                            ng4[i][j] = 4
                            sc4, _ = self.non_oo_simulate_move(move2, ng4)
                            score4 += 0.1 * sc4

            return (1 / zeros) * (score2 + score4)

        lst = []
        for move in self.MOVES:
            score = expectimax_rec(move, grid)
            if score:
                lst.append((move, score))

        lst = sorted(lst, key=lambda t: t[1], reverse=True)
        print(lst)
        return lst[0][0]


    def non_oo_simulate_move(self, move, grid):
        score = 0
        new_grid = grid
        if move == self.UP:
            score, new_grid = game.merge_up(grid)
        elif move == self.DOWN:
            score, new_grid = game.merge_down(grid)
        elif move == self.LEFT:
            score, new_grid = game.merge_left(grid)
        elif move == self.RIGHT:
            score, new_grid = game.merge_right(grid)
        return score, new_grid

