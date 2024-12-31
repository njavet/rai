import copy
import numpy as np
from rich.console import Console





def print_grid(grid: np.ndarray, console=None) -> None:
    if console is None:
        console = Console()
    for row in grid:
        console.print('|', end=' ')
        for val in row:
            console.print(str(val).rjust(4), end=' | ')
        console.print('\n' + 29*'-')


def utility(grid: np.array) -> float:
    # TODO analyze heuristics

    def helper(seq: np.ndarray) -> float:
        # number of zeros heuristic
        zeros = np.sum(seq == 0)

        # higher tiles are better
        rank = np.max(seq)
        if rank == 0:
            rw = 1
        else:
            rw = 1 / rank

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
