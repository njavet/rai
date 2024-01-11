import collections
import itertools

import game
import copy
import sys
import random

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
MOVES = [UP, DOWN, LEFT, RIGHT]


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
        self.dmax = self.max_distance()
        self.mscore = self.score()
        self.td = self.tile_distances()
        self.dall = 0
        self.d1 = 10
        self.d2 = 10
        self.d3 = 10
        self.d4 = 10

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
        return self.zeros - old_zeros

    def number_of_zeros(self):
        return len(self.tile_val_pos.get(0, []))

    def score(self):
        if not self.merges:
            return 0

        dix = collections.defaultdict(int)
        for row in self.grid:
            for val in row:
                dix[val] += 1

        new_dix = collections.defaultdict(int)
        for row in self.new_grid:
            for val in row:
                new_dix[val] += 1

        score = 0
        for k, v in dix.items():
            if k in new_dix:
                score += abs(k * (v - new_dix[k]))
            else:
                score += abs(k * v)
        return score / 2

    def max_distance(self):
        try:
            mv = max(self.tile_val_pos.keys())
            pos = self.tile_val_pos.get(mv)
            #pos = self.tile_val_pos[mv]
            return sum(pos[0])
        except ValueError:
            return 0

    def tile_distances(self):
        self.tile_val_pos.pop(0, None)
        named_tiles = {}
        for i, tile in enumerate(self.tile_val_pos.keys()):
            named_tiles['t' + str(i + 1)] = self.tile_val_pos[tile]

        dix = {}
        for name, positions in named_tiles.items():
            # all pairs of tile with the same value
            if len(positions) == 1:
                # drive towards upper left, TODO good ?
                dix[name] = sum(positions[0])
            elif len(positions) == 2:
                i0, j0 = positions[0]
                i1, j1 = positions[1]
                dd = (abs(i0 - i1) + abs(j0 - j1))
                if name == 't1':
                    self.d1 = dd
                if name == 't2':
                    self.d2 = dd
                elif name == 't3':
                    self.d3 = dd
                elif name == 't4':
                    self.d4 = dd
                else:
                    dix[name] = dd
            else:
                total = 0
                for (i0, j0), (i1, j1) in itertools.combinations(positions, r=2):
                    total += (abs(i0 - i1) + abs(j0 - j1))
                dix[name] = total
        return dix


def find_best_move(grid):
    simmoves = []
    for move in MOVES:
        sm = SimMove(move, grid)
        if sm.has_effect():
            simmoves.append(sm)

    for sm in simmoves:
        sm.dall = sum(sm.td.values())

    lst = sorted(simmoves, key=lambda sim: (sim.dmax,
                                            (-1)*sim.mscore,
                                            sim.d1,
                                            sim.d2,
                                            sim.d3,
                                            sim.d4,
                                            sim.dall,
                                            (-1)*sim.merges,
                                            (-1)*sim.zeros))

    for s in lst:
#        tds = ' '.join([f'{v:1.1f}' for v in s.td])
        print('dmax', s.dmax,
              'score', s.mscore,
              'd1', s.d1,
              'd2', s.d2,
              'd3', s.d3,
              'd4', s.d4,
              'all', s.dall,
              'merges', s.merges,
              'zeros', s.zeros)

    return lst[0].move


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

