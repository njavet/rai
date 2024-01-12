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

    def simulate_move(self, move, grid):
        grid_obj = game.Grid2048(grid, move)
        if move == self.UP:
            grid_obj.merge_up()
        elif move == self.DOWN:
            grid_obj.merge_down()
        elif move == self.LEFT:
            grid_obj.merge_left()
        elif move == self.RIGHT:
            grid_obj.merge_right()
        if grid != grid_obj.grid:
            return grid_obj

    def gen_simulation_lst(self, grid):
        lst = []
        for move in self.MOVES:
            grid_move = self.simulate_move(move, grid)
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
        simulations = self.gen_simulation_lst(grid)
        vals = self.gen_tile_list(simulations)

        lst = sorted(simulations,
                     key=lambda el: self.move_selection_priority(el,
                                                                 vals))

        console = Console()
        self.grid = game.Grid2048(grid)
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

    def find_best_move(self, grid):
        # return self.heuristic_move(grid)
        simulations = self.gen_simulation_lst(grid)
        for sim in simulations:
            sim.expectimax_score = self.expectimax(sim, 1, False)

        lst = sorted(simulations, key=lambda t: t.expectimax, reverse=True)
        print(lst)
        return lst[0].move


def find_best_move(grid):
    result = [score_top_level_move(i, grid) for i in range(4)]
    print('result', result)
    return result.index(max(result))


def score_top_level_move(move, grid):
    new_grid = game.simulate_move(move, grid)
    if grid == new_grid:
        return 0

    return expectimax(grid, depth=1, agent_play=False)


UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def expectimax(grid, depth, agent_play):
    if depth == 0:
        alpha = 0
        for move in range(4):
            new_grid = game.simulate_move(move, grid)
            alpha = min(alpha, game.compute_score(grid, new_grid))
        return alpha

    if agent_play:
        alpha = 0
        for move in range(4):
            new_grid = game.simulate_move(move, grid)
            alpha = max(alpha, expectimax(new_grid, depth-1, False))
        return alpha
    else:
        alpha = 0
        zero_cells = [(i, j) for i, row in enumerate(grid)
                      for j, val in enumerate(row) if val == 0]
        zeros = len(zero_cells)
        try:
            p = 1 / zeros
        except ZeroDivisionError:
            print('NO free cells')
            return expectimax(grid, depth-1, True)

        for i, j in zero_cells:
            ng2 = copy.deepcopy(grid)
            ng2[i][j] = 2
            alpha += p * 0.9 * expectimax(ng2, depth-1, True)

        for i, j in zero_cells:
            ng4 = copy.deepcopy(grid)
            ng4[i][j] = 4
            alpha += p * 0.1 * expectimax(ng4, depth-1, True)
        return alpha
