import random
import copy
import numpy as np
from rich.console import Console

# project imports
from rai.utils.helpers import random_argmax


class Agent:
    def __init__(self, depth: int = 3) -> None:
        self.depth = depth
        self.state = None
        self.simulator = Simulator()
        self.console = Console()

    def find_best_move(self, board: list[list[int]]) -> int:
        self.state = np.array(board, dtype=np.int16)
        result = np.array([self.score_top_level_move(i) for i in range(4)])

        if np.max(result) == 0:
            move = random.choice([0, 1, 2, 3])
        else:
            move = random_argmax(result)
        return move

    def score_top_level_move(self, move):
        self.simulator.simulate_move(self.state, move)
        if np.all(self.simulator.new_state == self.state):
            return 0

        return self.expectimax(self.simulator.new_state, self.depth, agent_play=False)

    def expectimax(self, grid: np.ndarray, depth: int, agent_play: bool) -> float:
        if depth == 0:
            return self.utility(grid)

        if agent_play:
            alpha = 0
            for move in range(4):
                self.simulator.simulate_move(grid, move)
                if not np.equal(self.simulator.new_state, grid).all():
                    alpha = max(alpha, self.expectimax(self.simulator.new_state,
                                                       depth-1,
                                                       False))
            return alpha
        else:
            expected_value = 0
            zero_cells = [(i, j) for i, row in enumerate(grid)
                          for j, val in enumerate(row) if val == 0]
            zeros = len(zero_cells)

            for i, j in zero_cells:
                ng2 = copy.deepcopy(grid)
                ng2[i][j] = 2
                expected_value += 0.9 * self.expectimax(ng2, depth-1, True)

                ng4 = copy.deepcopy(grid)
                ng4[i][j] = 4
                expected_value += 0.1 * self.expectimax(ng4, depth-1, True)
            return (1 / zeros) * expected_value

    @staticmethod
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

    def print_grid(self):
        for row in self.state:
            self.console.print('|', end=' ')
            for val in row:
                self.console.print(str(val).rjust(4), end=' | ')
            self.console.print('\n' + 29*'-')


class Simulator:
    def __init__(self):
        self.state = None
        self.new_state = None
        self.reward = 0

    def simulate_move(self, state, move):
        self.state = state
        if move == 0:
            self.merge_left()
        elif move == 1:
            self.merge_down()
        elif move == 2:
            self.merge_right()
        elif move == 3:
            self.merge_up()

    def merge_left(self):

        def merge_seq_to_left(seq, acc, seq_r: float = 0) -> tuple[list[int], float]:
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
        for i, row in enumerate(self.state):
            merged, r = merge_seq_to_left([x for x in row if x != 0], [])
            zeros = len(row) - len(merged)
            merged_zeros = merged + zeros * [0]
            new_grid.append(merged_zeros)
            reward += r
        self.new_state = np.array(new_grid, dtype=np.int16)
        self.reward = reward

    def merge_right(self):
        self.state = self.state[:, ::-1]
        self.merge_left()
        self.new_state = self.new_state[:, ::-1]

    def merge_up(self):
        self.state = self.state.transpose()
        self.merge_left()
        self.new_state = self.new_state.transpose()

    def merge_down(self):
        self.state = self.state.transpose()
        self.merge_right()
        self.new_state = self.new_state.transpose()
