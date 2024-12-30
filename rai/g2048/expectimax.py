import copy
import numpy as np
from rich.console import Console


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
        return merge_left(grid)
    elif move == 1:
        return merge_down(grid)
    elif move == 2:
        return merge_right(grid)
    elif move == 3:
        return merge_up(grid)


def print_grid(grid: np.ndarray, console=None) -> None:
    if console is None:
        console = Console()
    for row in grid:
        console.print('|', end=' ')
        for val in row:
            console.print(str(val).rjust(4), end=' | ')
        console.print('\n' + 29*'-')


def utility(grid: np.array) -> float:

    def helper(seq: np.ndarray) -> float:
        # TODO fix sequence vs grid

        # number of zeros heuristic
        zeros = np.sum(seq == 0)

        # higher tiles are better
        rank = np.max(seq)
        try:
            rw = 1 / rank
        except ZeroDivisionError:
            rw = 1

        # large tiles on the edge
        ind = np.where(seq == rank)[0][0]
        if ind == 0 or ind == 3:
            edge = 1 - rw
        else:
            edge = 0

        # monotonous
        mono = 0
        mon_inc = np.all([val <= seq[i + 1] for i, val in enumerate(seq[:-1])])
        mon_dec = np.all([seq[i + 1] <= val for i, val in enumerate(seq[:-1])])
        if mon_inc:
            mono += 2
        if mon_dec:
            mono += 2

        adj = 0
        for i, val in enumerate(seq[1:]):
            if np.all(val == seq[i + 1]):
                adj += 1 - rw

        return zeros + edge + mono + adj

    tmp = np.sum([helper(grid[:, i]) for i in range(4)])
    return tmp + np.sum([helper(grid[i, :]) for i in range(4)])


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
