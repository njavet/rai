import random
import copy
import numpy as np
import itertools
from rich.console import Console


def add_random_tile(grid: np.ndarray) -> np.ndarray:
    inds = [(i, j) for (i, j) in itertools.product(range(4), repeat=2)
            if grid[i][j] == 0]
    if len(inds) > 0:
        i, j = random.choice(inds)
        value = np.random.choice([2, 4], p=[0.9, 0.1])
        grid[i, j] = value
        return grid


def merge_left(grid: np.ndarray) -> tuple[np.ndarray, float]:

    def merge_seq_to_left(seq, acc, seq_r=0):
        if not seq:
            return acc, seq_r

        x = seq[0]
        if len(seq) == 1:
            return acc + [x], seq_r

        if x == seq[1]:
            return merge_seq_to_left(seq[2:], acc + [2 * x], seq_r + 2 * x)
        else:
            return merge_seq_to_left(seq[1:], acc + [x], seq_r)

    new_grid = []
    reward = 0
    for i, row in enumerate(grid):
        merged, r = merge_seq_to_left([x for x in row if x != 0], [])
        zeros = len(row) - len(merged)
        merged_zeros = merged + zeros * [0]
        new_grid.append(merged_zeros)
        reward += r
    return np.array(new_grid, dtype=np.int16), reward


def merge_right(grid: np.ndarray) -> tuple[np.ndarray, float]:
    new_grid, reward = merge_left(np.array([row[::-1] for row in grid]))
    return np.array([row[::-1] for row in new_grid], dtype=np.int16), reward


def merge_up(grid: np.ndarray) -> tuple[np.ndarray, float]:
    new_grid, reward = merge_left(grid.transpose())
    return new_grid.transpose(), reward


def merge_down(grid: np.ndarray) -> tuple[np.ndarray, float]:
    new_grid, reward = merge_right(grid.transpose())
    return new_grid.transpose(), reward


def simulate_move(grid: np.ndarray, move: int) -> tuple[np.ndarray, float]:
    if move == 0:
        return merge_up(grid)
    elif move == 1:
        return merge_down(grid)
    elif move == 2:
        return merge_left(grid)
    elif move == 3:
        return merge_right(grid)


def available_moves(grid: np.ndarray) -> list:
    moves = []
    mg0, _ = merge_up(grid)
    if not np.array_equal(mg0, grid):
        moves.append(0)
    mg1, _ = merge_down(grid)
    if not np.array_equal(mg1, grid):
        moves.append(1)
    mg2, _ = merge_left(grid)
    if not np.array_equal(mg2, grid):
        moves.append(2)
    mg3, _ = merge_right(grid)
    if not np.array_equal(mg3, grid):
        moves.append(3)
    return moves


def is_move_available(grid: np.ndarray, move: int) -> bool:
    am = available_moves(grid)
    return move in am


def print_grid(grid: np.ndarray, console=None) -> None:
    if console is None:
        console = Console()
    for row in grid:
        console.print('|', end=' ')
        for val in row:
            console.print(str(val).rjust(4), end=' | ')
        console.print('\n' + 29*'-')


def utility(grid: np.ndarray) -> float:

    # number of zeros heuristic
    zeros = np.sum(grid == 0)

    # higher tiles are better
    rank = np.max(grid)
    try:
        rw = 1 / rank
    except ZeroDivisionError:
        rw = 1

    # large tiles on the edge
    ind = np.where(grid == rank)[0][0]
    if ind == 0 or ind == 3:
        edge = 1 - rw
    else:
        edge = 0

    # monotonous
    mono = 0
    mon_inc = np.all([val <= grid[i + 1] for i, val in enumerate(grid[:-1])])
    mon_dec = np.all([grid[i + 1] <= val for i, val in enumerate(grid[:-1])])
    if mon_inc:
        mono += 2
    if mon_dec:
        mono += 2

    adj = 0
    for i, val in enumerate(grid[1:]):
        if np.all(val == grid[i + 1]):
            adj += 1 - rw

    return zeros + edge + mono + adj


def expectimax(grid: np.ndarray, depth: int, agent_play: bool) -> float:
    if depth == 0:
        return utility(grid)

    if agent_play:
        alpha = 0
        for move in range(4):
            new_grid, _ = simulate_move(grid, move)
            if not np.equal(new_grid, grid).all():
                alpha = max(alpha, expectimax(new_grid, depth-1, False))
        return alpha
    else:
        expected_value = 0
        zero_cells = [(i, j) for i, row in enumerate(grid)
                      for j, val in enumerate(row) if val == 0]
        zeros = len(zero_cells)

        for i, j in zero_cells:
            ng2 = copy.deepcopy(grid)
            ng2[i][j] = 2
            expected_value += 0.9 * expectimax(ng2, depth-1, True)

            ng4 = copy.deepcopy(grid)
            ng4[i][j] = 4
            expected_value += 0.1 * expectimax(ng4, depth-1, True)
        return (1 / zeros) * expected_value

