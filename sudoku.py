
"""
a constraint satisfaction problem consists of three components:
    X: set of variables
    D:  set of domains, one for each variable
    C: constraints that specify allowable combinations of values

"""
import itertools
import string
import collections


aima = [[0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]]


grid = [[0, 0, 0, 0, 0, 6, 0, 7, 0],
        [8, 0, 1, 4, 7, 3, 0, 0, 0],
        [7, 0, 0, 0, 0, 1, 9, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 9],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
        [9, 0, 0, 5, 0, 8, 0, 0, 4],
        [4, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 6, 2, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 4, 0, 0]]


class Agent:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.moves = 0

    def get_neighbors(self, i, j):
        neighbors = [(i, k) for k in range(0, i)]
        neighbors = neighbors + [(i, k) for k in range(i+1, 9)]

        neighbors = neighbors + [(k, j) for k in range(0, j)]
        neighbors = neighbors + [(k, j) for k in range(j+1, 9)]

        rs = i - i % 3
        cs = j - j % 3
        for ii in range(rs, rs + 3):
            for jj in range(cs, cs + 3):
                if (ii, jj) not in neighbors:
                    if (ii, jj) != (i, j):
                        neighbors.append((ii, jj))
        return [(ii, jj) for ii, jj in neighbors if (ii, jj) in self.zero_cells.keys()]


    def get_row_vals(self, i):
        return self.grid[i]

    def is_safe_row(self, i, val):
        return val not in self.grid[i]
    
    def get_col_vals(self, j):
        return [row[j] for row in self.grid]

    def is_safe_col(self, j, val):
        return val not in [row[j] for row in self.grid]

    def get_box_vals(self, i, j):
        row_start = i - i % 3
        col_start = j - j % 3
        box = []
        for ii in range(row_start, row_start+3):
            for jj in range(col_start, col_start+3):
                box.append(self.grid[ii][jj])
        return box

    def is_safe_box(self, i, j, val):
        row_start = i - i % 3
        row_ind = [row_start, row_start + 1, row_start + 2]
        col_start = j - j % 3
        col_ind = [col_start, col_start + 1, col_start + 2]
        return val not in [self.grid[ri][ci]
                           for (ri, ci) in itertools.product(row_ind, col_ind)]

    def get_free_values(self, i, j):
        a = self.get_row_vals(i)
        b = self.get_col_vals(j)
        c = self.get_box_vals(i, j)
        d = set(a + b + c)
        return [val for val in range(1, 10) if val not in d]

    def is_safe(self, i, j, val):
        return (
                self.is_safe_row(i, val) and
                self.is_safe_col(j, val) and
                self.is_safe_box(i, j, val)
        )

    def arc_constraints(self):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    free_values = self.get_free_values(i, j)
                    if len(free_values) == 1:
                        self.grid[i][j] = free_values[0]
                        self.moves += 1
                        self.arc_constraints()

    def get_zero_cell(self):
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    return i, j

    def print_board(self):
        for i, row in enumerate(self.grid):
            print(' | '.join([' '.join([str(val) for val in row[0:3]]),
                              ' '.join([str(val) for val in row[3:6]]),
                              ' '.join([str(val) for val in row[6:]])]))
            if i in [2, 5]:
                print('---------------------')


    def backtrack_naive(self):
        try:
            i, j = self.get_zero_cell()
        except TypeError:
            return True

        for val in range(1, 10):
            if self.is_safe(i, j, val):
                self.grid[i][j] = val
                self.moves += 1

                if self.backtrack_naive():
                    return True

                self.grid[i][j] = 0

    def backtrack(self):
        try:
            i, j = self.get_zero_cell()
        except TypeError:
            return True
    
        for val in self.get_free_values(i, j):
            self.grid[i][j] = val
            self.moves += 1

            if self.backtrack():
                return True

            self.grid[i][j] = 0
        

    def solve_0(self):
        self.backtrack_naive()
        print('solve_0 moves', self.moves)

    def solve_1(self):
        self.backtrack()
        print('solve_1 moves', self.moves)

    def solve_2(self):
        self.arc_constraints()
        self.backtrack_naive()
        print('solve_2 moves', self.moves)

    def solve_3(self):
        self.arc_constraints()
        self.backtrack()
        print('solve_3 moves', self.moves)


agent0 = Agent(grid)
agent0.solve_0()

agent1 = Agent(grid)
agent1.solve_1()

agent2 = Agent(grid)
agent2.solve_2()

agent3 = Agent(grid)
agent3.solve_3()



