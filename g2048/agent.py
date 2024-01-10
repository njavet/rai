import collections
import itertools

import game
import copy
import sys
import random

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
MOVES = [UP, DOWN, LEFT, RIGHT]


# goals:
# highest tile in left upper corner
# as many empty cells as possible
# as many merges as possible 


class SimMove:
    def __init__(self, move, grid):
        self.move = move
        self.grid = grid
        self.new_grid = simulate_move(move, grid)
        self.tile_val_pos = self.gen_tile_dict()
        # secondary
        self.zeros = self.number_of_zeros()
        self.merges = self.number_of_merges()
        # primary selection criteria
        self.td_dix = self.tile_distances()
        self.td = list(self.td_dix.values())

    def gen_tile_dict(self):
        dix = collections.defaultdict(list)
        for i, row in enumerate(self.new_grid):
            for j, val in enumerate(row):
                dix[val].append((i, j))
        return {val: sorted(dix[val]) for val in sorted(dix, reverse=True)}

    def has_effect(self):
        return self.grid != self.new_grid

    def number_of_merges(self):
        old_zeros = sum(row.count(0) for row in self.grid)
        return self.number_of_zeros() - old_zeros

    def number_of_zeros(self):
        return -1 * len(self.tile_val_pos.get(0, []))

    def tile_distances(self):
        self.tile_val_pos.pop(0, None)
        self.tile_val_pos.pop(2, None)
        self.tile_val_pos.pop(4, None)
        self.tile_val_pos.pop(8, None)

        tile_dist = collections.defaultdict(int)
        for tile, positions in self.tile_val_pos.items():
            # all pairs of tile with the same value
            if len(positions) == 1:
                tile_dist[tile] = sum(positions[0])
            else:
                for (i0, j0), (i1, j1) in itertools.combinations(positions, r=2):
                    tile_dist[tile] += abs(i0 - i1) + abs(j0 - j1)
        return tile_dist


class State:
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.simmoves = self.compute_grids()

    def compute_grids(self):
        simmoves = {}
        for move in MOVES:
            sm = SimMove(move, self.grid)
            if sm.has_effect():
                simmoves[move] = sm
        return simmoves

    def chose_move(self):
        lst = sorted(self.simmoves.values(),
                      key=lambda sm: (sm.td, sm.merges, sm.zeros))
        for s in lst:
            tds = ' '.join([f'{v:1.1f}' for k, v in s.td_dix.items()])
            print('TD', tds, '\tMERGES', s.merges, 'ZEROS', s.zeros)
        return lst[0].move


def find_best_move(grid):
    return State(grid).chose_move()


def random_move():
    return random.choice([UP, DOWN, LEFT, RIGHT])


def simulate_move(move, grid):
    if move == UP:
        return game.merge_up(grid)
    elif move == DOWN:
        return game.merge_down(grid)
    elif move == LEFT:
        return game.merge_left(grid)
    elif move == RIGHT:
        return game.merge_right(grid)
    else:
        sys.exit('invalid move')


def score_toplevel_move(move, grid):
    # expectimax
    newgrid = simulate_move(move, grid)

    if game.equal_grids(grid, newgrid):
        return 0

