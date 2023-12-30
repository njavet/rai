import string
import collections
import csp

"""
a constraint satisfaction problem consists of three components:
    X: set of variables
    D:  set of domains, one for each variable
    C: constraints that specify allowable combinations of values


assignment: a : X -> D*

"""


grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 8, 5],
        [0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 7, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 3],
        [0, 0, 2, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 9]]


aima = [[0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]]


zhaw = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]]


class SudokuCSP(csp.CSP):
    def __init__(self, grid):
        super().__init__()
        self.grid = [row[:] for row in grid]
        self.construct_variables()
        self.assign_neighbors()
        self.construct_constraints()

    def construct_variables(self):
        self.variables = {}
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                name = string.ascii_uppercase[0:9][i] + str(j)
                if val == 0:
                    domain = list(range(1, 10))
                    self.variables[i, j] = csp.Variable(name, domain)
                else:
                    domain = [val]
                    self.variables[i, j] = csp.Variable(name, domain)
                    self.variables[i, j].assigned = val

    def assign_neighbors(self):
        for (i, j), var in self.variables.items():
            var.neighbors = self.get_neighbors(i, j)

    def construct_constraints(self):
        self.constraints = []
        row = collections.defaultdict(list)
        col = collections.defaultdict(list)
        box = collections.defaultdict(list)
        for (i, j), var in self.variables.items():
            row[i].append(var)
            col[j].append(var)
            ii = i - i % 3
            jj = j - j % 3
            box[ii, jj].append(var)
        for rc in row.values():
            self.constraints.append(csp.AllDiff(rc))
        for cc in col.values():
            self.constraints.append(csp.AllDiff(cc))
        for bc in box.values():
            self.constraints.append(csp.AllDiff(bc))

    def get_row_indexes(self, i, j):
        a = [(i, k) for k in range(0, j)]
        b = [(i, k) for k in range(j+1, 9)]
        assert(len(a + b) == 8)
        return a + b

    def get_col_indexes(self, i, j):
        a = [(k, j) for k in range(0, i)]
        b = [(k, j) for k in range(i+1, 9)]
        assert(len(a + b) == 8)
        return a + b

    def get_box_indexes(self, i, j):
        rs = i - i % 3
        cs = j - j % 3
        box = []
        for ii in range(rs, rs + 3):
            for jj in range(cs, cs + 3):
                if ii != i and jj != j:
                    box.append((ii, jj))
        assert(len(box) == 4)
        return box

    def get_neighbor_indexes(self, i, j):
        a = self.get_row_indexes(i, j)
        b = self.get_col_indexes(i, j)
        c = self.get_box_indexes(i, j)
        assert(len(a + b + c) == 20)
        return a + b + c

    def get_neighbors(self, i, j):
        neighbors = []
        for ii, jj in self.get_neighbor_indexes(i, j):
            neighbors.append(self.variables[ii, jj])
        return neighbors

    def solve(self):
        print('applying AC3...')
        queue = [(Xi, Xj) for Xi in self.variables.values() for Xj in Xi.neighbors]
        self.AC3(queue)

        for var in self.variables.values():
            if len(var.domain) == 1:
                var.assigned = var.domain[0]
                var.domain = []

        for con in self.constraints:
            while con.prune():
                pass

        for (i, j), var in self.variables.items():
            if var.assigned:
                self.grid[i][j] = var.assigned



sudoku = SudokuCSP(grid)
for row in sudoku.grid:
    print(row)
sudoku.solve()
for row in sudoku.grid:
    print(row)

"""
for var in sudoku.variables.values():
    if var.name == 'I7':
        print(var.name, var.domain)
        for n in var.neighbors:
            print(n.name, n.domain)


print('--')
for var in sudoku.variables.values():
    if var.name == 'I7':
        print(var.name, var.domain)
        for n in var.neighbors:
            print(n.name, n.domain)

print('--')
for con in sudoku.constraints:
    print('constraint', len(con.variables))
    for var in con.variables:
        print(var.name, var.domain, )


for var in sudoku.variables.values():
    if var.name == 'G6':
        print(var.name, var.domain)
    if var.name == 'H6':
        print(var.name, var.domain)
    if var.name == 'H7':
        print(var.name, var.domain)
    if var.name == 'H8':
        print(var.name, var.domain)
    if var.name == 'I6':
        print(var.name, var.domain)
    if var.name == 'I7':
        print(var.name, var.domain)

"""
