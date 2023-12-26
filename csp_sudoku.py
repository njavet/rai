
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


grid = [0, 0, 0, 0, 0, 6, 0, 7, 0,
        8, 0, 1, 4, 7, 3, 0, 0, 0,
        7, 0, 0, 0, 0, 1, 9, 0, 0,
        6, 0, 0, 0, 0, 0, 0, 0, 9,
        0, 5, 0, 0, 0, 0, 0, 0, 0,
        9, 0, 0, 5, 0, 8, 0, 0, 4,
        4, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 6, 2, 0, 3, 0, 0, 0, 0,
        0, 0, 0, 2, 0, 0, 4, 0, 0]


class Agent:
    def __init__(self, grid):
        self.grid = grid
        self.zero_cells = self.get_zero_cells()
    
    def get_zero_cells(self):
        zeros = {}
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == 0:
                    zeros[i, j] = self.get_free_values(i, j)
        return zeros

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

    def get_col_vals(self, j):
        return [row[j] for row in self.grid]

    def get_box_vals(self, i, j):
        row_start = i - i % 3
        col_start = j - j % 3
        box = []
        for ii in range(row_start, row_start+3):
            for jj in range(col_start, col_start+3):
                box.append(self.grid[ii][jj])
        return box

    def get_free_values(self, i, j):
        a = self.get_row_vals(i)
        b = self.get_col_vals(j)
        c = self.get_box_vals(i, j)
        d = set(a + b + c)
        return [val for val in range(1, 10) if val not in d]

    def ac3(self, queue):
        while queue:
            i, j, ii, jj = queue.pop()
            if self.revise(i, j, ii, jj):
                if len(self.zero_cells[i, j]) == 0:
                    return False
                for x, y in self.get_neighbors(i, j):
                    if (x, y) != (ii, jj):
                        queue.append((x, y, i, j))

        return True

    def revise(self, i, j, ii, jj):
        revised = False
        di = self.zero_cells[i, j]
        dj = self.zero_cells[ii, jj]
        for x in di:
            if len(dj) == 1 and dj[0] == x:
                ind = di.index(x)
                del di[ind]
                revised = True
        return revised

    def solve(self):
        queue = []
        for i, j in self.zero_cells.keys():
            neighbors = self.get_neighbors(i, j)
            for ii, jj in neighbors:
                queue.append((i, j, ii, jj))
        self.ac3(queue)



agent = Agent(aima)

for (i, j), val in agent.zero_cells.items():
    print(i, j, val)

agent.solve()
print('---------')
for (i, j), val in agent.zero_cells.items():
    print(i, j, val)

