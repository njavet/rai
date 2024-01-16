import collections
from rich.text import Text
from rich.console import Console
import itertools
import math
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import functools
import operator
import dqn

import game
import copy
import sys
import random
import torch


model = dqn.DQN()
model.load_state_dict(torch.load('policy_state_dict.pth'))

class Memoize:
    def __init__(self, func):
        self.func = func
        self.memo = {}

    def __call__(self, *args, **kwargs):
        if args not in self.memo:
            self.memo[args] = self.func(*args)
        return self.memo[args]


class Node:
    def __init__(self, grid, move=None):
        if move is None:
            self.move = -1
        else:
            self.move = move

        self.grid = grid
        self.grid_tuple = self.convert_grid_2_tuple()
        self.num = 0
        self.path = []

    def convert_grid_2_tuple(self):
        return functools.reduce(operator.add,
                                [tuple(row) for row in self.grid])

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.grid_tuple == other.grid_tuple
        else:
            return False

    def __hash__(self):
        return hash(self.grid_tuple)

# heuristics from stackover flow post:
# bonus for zero cells
# large tiles on the edge
# penalty for non mononic rows / cols with increasing ranks
# number of potential merges (adjacent equal values) in addition
# to zero cells -> this increases delayed merges

# CMA-ES adjust weights -> maybe RL ?

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

b = 0

def find_best_move_0(grid):
    global b
    b = 0
    result = [score_top_level_move(i, grid) for i in range(4)]
    #game.print_grid(grid)
    print('result', result)
    print('branches', b)

    if max(result) == 0:
        move = random.choice([0, 1, 2, 3])
    else:
        move = result.index(max(result))
    return move


def find_best_move(grid):
    g = np.array(grid).reshape(16)
    state = torch.tensor(g, dtype=torch.float32)
    res = model(state)
    print('tensor', res)
    move = torch.argmax(res).item()
    print('move', move)
    return move


def score_top_level_move(move, grid, depth=4):
    new_grid = game.simulate_move(move, grid)
    if new_grid == grid:
        return 0

    #print('MOVE', move)
    node = Node(new_grid, move)
    node.path = [move]
    node.num = move
    return expectimax(node, depth, agent_play=False)


@Memoize
def score_seq(seq):
    """
        the goal is to find the correct weights to combine the obviously
        good heuristics:
        zeros: number of empty cells, the more, the better
        rank: maximum tile, the higher, the better
        edge / corner: large tiles in corner or at the edges
        monotony: a monotonously decreasing / increasing board is easier to merge
        adjacency: the more tiles with the same value are close together, the better
        how important are the values of the tiles in the mono / adj, edge score ?

        return bias +
               w0 * zeros +
               w1 * rank +
               w2 * edge +
               w3 * mono +
               w4 * adj
    :param seq:
    :return:
    """

    # number of zeros heuristic
    zeros = seq.count(0)

    # higher tiles are better
    rank = max(seq)
    try:
        rw = 1 / rank
    except ZeroDivisionError:
        rw = 1

    # large tiles on the edge
    ind = seq.index(rank)
    if ind == 0 or ind == 3:
        edge = 1 - rw
    else:
        edge = 0

    # monotonous
    mono = 0
    mon_inc = all([val <= seq[i + 1] for i, val in enumerate(seq[:-1])])
    mon_dec = all([seq[i + 1] <= val for i, val in enumerate(seq[:-1])])
    if mon_inc:
        mono += 2
    if mon_dec:
        mono += 2

    adj = 0
    for i, val in enumerate(seq[1:]):
        if val == seq[i + 1]:
            adj += 1 - rw

    return zeros + edge + mono + adj


@Memoize
def utility(node):
    if not game.move_available(node.grid):
        print('WILL encounter game over soon')
        return 0
    score = 0
    for row in node.grid:
        score += score_seq(tuple(row))
    for col in zip(*node.grid):
        score += score_seq(tuple(col))
    #print('score:', score)
    return score


def expectimax(node, depth, agent_play):
    if depth == 0:
        global b
        b += 1
        #print(utility(node))
        assert(node.move >= 0)
        return utility(node)

    if agent_play:
        alpha = 0
        for move in range(4):
            new_grid = game.simulate_move(move, node.grid)
            if new_grid != node.grid:
                next_node = Node(new_grid, move)
                alpha = max(alpha, expectimax(next_node, depth-1, False))
        #print('random node alpha', alpha)
        return alpha
    else:
        expected_value = 0
        zero_cells = [(i, j) for i, row in enumerate(node.grid)
                      for j, val in enumerate(row) if val == 0]
        zeros = len(zero_cells)

        for i, j in zero_cells:
            ng2 = copy.deepcopy(node.grid)
            ng2[i][j] = 2
            next_node2 = Node(ng2)
            expected_value += 0.9 * expectimax(next_node2, depth-1, True)

            ng4 = copy.deepcopy(node.grid)
            ng4[i][j] = 4
            next_node4 = Node(ng4)
            expected_value += 0.1 * expectimax(next_node4, depth-1, True)
        #print('expected value', (1 / zeros) * expected_value)
        return (1 / zeros) * expected_value

