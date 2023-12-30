import string
import collections
from rich.console import Console
from rich.text import Text


import csp


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



class SudokuGrid:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]

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

    def print_grid(self):
        for i, row in enumerate(self.grid):
            s0 = ' '.join([str(val) for val in row[0:3]])
            s1 = ' '.join([str(val) for val in row[3:6]])
            s2 = ' '.join([str(val) for val in row[6:]])
            s3 = ' | '.join([s0, s1, s2])
            print(' ' + s3)
            if i in [2, 5]:
                print(23*'-')



class SudokuCSP(csp.CSP):
    def __init__(self, grid):
        super().__init__()
        self.grid = SudokuGrid(grid)
        self.construct_variables()
        self.assign_neighbors()
        self.construct_constraints()

    def construct_variables(self):
        self.variables = {}
        for i, row in enumerate(self.grid.grid):
            for j, val in enumerate(row):
                name = string.ascii_uppercase[0:9][i] + str(j)
                if val == 0:
                    domain = list(range(1, 10))
                    self.variables[i, j] = csp.Variable(name, domain)
                else:
                    domain = [val]
                    self.variables[i, j] = csp.Variable(name, domain)
                    self.variables[i, j].assigned = val

    def get_neighbors(self, i, j):
        neighbors = []
        for ii, jj in self.grid.get_neighbor_indexes(i, j):
            neighbors.append(self.variables[ii, jj])
        return neighbors

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
        for i, rc in enumerate(row.values()):
            self.constraints.append(csp.AllDiff('R' + str(i), rc))
        for i, cc in enumerate(col.values()):
            self.constraints.append(csp.AllDiff('C' + str(i), cc))
        for i, bc in enumerate(box.values()):
            self.constraints.append(csp.AllDiff('B' + str(i), bc))

    def print_variables(self):
        console = Console()
        s = Text('   | 0 1 2 | 3 4 5 | 6 7 8 ', style='bold white')
        console.print(s)
        console.print(' ' + 25 * '-')
        for i, row in enumerate(self.grid.grid):
            a = string.ascii_uppercase[0:9][i]
            t = Text(' ' + a + ' | ', style='bold white')
            for j, val in enumerate(row):
                var = self.variables[i, j]
                if var.assigned and var.step == 0:
                    t.append(str(var.assigned) + ' ', style='red')
                elif var.assigned and var.step == 1:
                    t.append(str(var.assigned) + ' ', style='green')
                elif var.assigned and var.step == 2:
                    t.append(str(var.assigned) + ' ', style='blue')
                elif var.assigned:
                    t.append(str(var.assigned) + ' ', style='bold green')

                else:
                    t.append('0 ', style='bold grey')
                if j in [2, 5]:
                    t.append('| ')
            console.print(t)
            if i in [2, 5]:
                console.print(' ' + 25 * '-')

    def assign(self):
        n = 0
        for var in self.variables.values():
            if var.name == 'G1':
                print('in assign', var.name, var.domain)
            if not var.assigned and len(var.domain) == 1:
                n += 1
                var.step += 1
                var.assigned = var.domain[0]
            elif not var.assigned:
                var.step += 1
        return n

    def solve(self):
        self.AC3()
        n = self.assign()

        if n:
            print('first AC3, assigned: ', n)
            self.print_variables()

        for con in self.constraints:
            lst = con.reduce_constraint_variables_domain()
            n = self.assign()
            queue = [(Xi, Xj) for Xi in lst for Xj in Xi.neighbors]
            queue2 = [(Xj, Xi) for Xi in lst for Xj in Xi.neighbors]
            self.AC3(queue + queue2)
            if n:
                self.print_variables()


sudoku = SudokuCSP(grid)
#sudoku = SudokuCSP(aima)
#sudoku = SudokuCSP(zhaw)
print('start grid')
sudoku.print_variables()
sudoku.solve()
sudoku.print_variables()


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
