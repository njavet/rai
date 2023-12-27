import string
import collections

"""
a constraint satisfaction problem consists of three components:
    X: set of variables
    D:  set of domains, one for each variable
    C: constraints that specify allowable combinations of values

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


class Variable:
    def __init__(self, name: str, domain: list[int]):
        self.name = name
        self.domain = domain 
        self.neighbors = None

    def is_solved(self):
        return len(self.domain) == 1

    def is_invalid(self):
        return len(self.domain) == 0


class SudokuCSP:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.variables = self.construct_variables()
        self.assign_neighbors()

    def construct_variables(self):
        variables = {}
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                name = string.ascii_uppercase[0:9][i] + str(j)
                if val == 0:
                    domain = list(range(1, 10))
                else:
                    domain = [val]
                variables[i, j] = Variable(name, domain)
        return variables 

    def assign_neighbors(self):
        for (i, j), var in self.variables.items():
            var.neighbors = self.get_neighbors(i, j)

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

    def revise(self, Xi, Xj):
        revised = False
        for i, x in enumerate(Xi.domain):
            if all([x == y for y in Xj.domain]):
                del Xi.domain[i]
                revised = True
        return revised

    def AC3(self, queue=None):
        if queue is None:
            queue = [(Xi, Xk) for Xi in self.variables.values() for Xk in Xi.neighbors]
        while queue:
            Xi, Xj = queue.pop()
            if self.revise(Xi, Xj):
                if len(Xi.domain) == 0:
                    return False
                for Xk in [Xn for Xn in Xi.neighbors if Xn.name != Xj.name]:
                    queue.append((Xk, Xi))
        return True

    def solve(self):
        self.AC3()
        units = self.construct_units()

        for (i, j), var in self.variables.items():
            row_unit = self.get_row_indexes(i, j)
            row_dix = collections.defaultdict(int)
            for ri, rj in row_unit:
                row_var = self.variables[ri, rj]
                for num in row_var.domain:
                    row_dix[num] += 1
            
            col_unit = self.get_col_indexes(i, j)
            box_unit = self.get_box_indexes(i, j)


        for unit in units:
            for k, v in unit.value_dix.items():
                if v == 1:

                print(k, v)



sudoku = SudokuCSP(grid)
for var in sudoku.variables.values():
    if var.name == 'I7':
        for n in var.neighbors:
            print(n.name, n.domain)
        print(var.domain)

sudoku.solve()

"""
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
