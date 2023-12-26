import itertools
import collections


grid = [[0, 0, 0, 0, 2, 0, 5, 0, 0],
        [0, 0, 8, 5, 0, 9, 0, 0, 2],
        [0, 4, 0, 3, 8, 0, 1, 9, 0],
        [3, 5, 0, 1, 7, 8, 9, 0, 0],
        [7, 6, 0, 0, 0, 3, 8, 5, 1],
        [8, 0, 9, 0, 0, 0, 4, 7, 3],
        [0, 0, 7, 2, 0, 1, 6, 0, 0],
        [1, 2, 0, 8, 9, 5, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 0]]

amia = [[0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]]


class Agent:
    def __init__(self):
        self.grid = grid
        self.moves = 0

    def get_zero_cell(self):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    return i, j
    
    def is_safe_row(self, i, val):
        return val not in self.grid[i]
    
    def is_safe_col(self, j, val):
        return val not in [row[j] for row in self.grid]

    def is_safe_box(self, i, j, val):
        row_start = i - i % 3
        row_ind = [row_start, row_start + 1, row_start + 2]
        col_start = j - j % 3
        col_ind = [col_start, col_start + 1, col_start + 2]
        return val not in [self.grid[ri][ci] 
                           for (ri, ci) in itertools.product(row_ind, col_ind)]

    def is_safe(self, i, j, val):
        return (
                self.is_safe_row(i, val) and
                self.is_safe_col(j, val) and
                self.is_safe_box(i, j, val)
        )

    def print_board(self):
        for i, row in enumerate(self.grid):
            print(' | '.join([' '.join([str(val) for val in row[0:3]]),
                              ' '.join([str(val) for val in row[3:6]]),
                              ' '.join([str(val) for val in row[6:]])]))
            if (i + 1) % 3 == 0:
                print('---------------------')

    def solve(self):
        try:
            i, j = self.get_zero_cell()
        except TypeError:
            return True

        for val in range(1, 10):
            if self.is_safe(i, j, val):
                self.grid[i][j] = val
                self.moves += 1

                if self.solve():
                    return True

                self.grid[i][j] = 0
    


ag = Agent()
ag.solve()
ag.print_board()
print('backtrack', ag.moves)

"""
AIMA problem solving agents 
 a search problem can be defined as follows:

  - set of initial states
  - initial state
  - goal state
  - available actions for the agent 
  - transition model
  - action cost function

"""
