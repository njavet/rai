import string
import collections
import itertools
from rich.console import Console
from rich.text import Text


import csp

#Grid 06
#Grid 07
#Grid 10
#Grid 25
#Grid 42
#Grid 43
#Grid 47
#Grid 48
#Grid 49
#Grid 50

grid06 = [[1, 0, 0, 9, 2, 0, 0, 0, 0],
          [5, 2, 4, 0, 1, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 0],
          [0, 5, 0, 0, 0, 8, 1, 0, 2],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [4, 0, 2, 7, 0, 0, 0, 9, 0],
          [0, 6, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 3, 0, 9, 4, 5],
          [0, 0, 0, 0, 7, 1, 0, 0, 6]]


grid07 = [[0, 4, 3, 0, 8, 0, 2, 5, 0],
          [6, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 1, 0, 9, 4],
          [9, 0, 0, 0, 0, 4, 0, 7, 0],
          [0, 0, 0, 6, 0, 8, 0, 0, 0],
          [0, 1, 0, 2, 0, 0, 0, 0, 3],
          [8, 2, 0, 5, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 5],
          [0, 3, 4, 0, 9, 0, 7, 1, 0]]


grid10 = [[0, 0, 1, 9, 0, 0, 0, 0, 3],
          [9, 0, 0, 7, 0, 0, 1, 6, 0],
          [0, 3, 0, 0, 0, 5, 0, 0, 7],
          [0, 5, 0, 0, 0, 0, 0, 0, 9],
          [0, 0, 4, 3, 0, 2, 6, 0, 0],
          [2, 0, 0, 0, 0, 0, 0, 7, 0],
          [6, 0, 0, 1, 0, 0, 0, 3, 0],
          [0, 4, 2, 0, 0, 7, 0, 0, 6],
          [5, 0, 0, 0, 0, 6, 8, 0, 0]]

grid55 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        self.construct_variables(grid)
        self.construct_constraints()

    def construct_variables(self, grid):
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                name = string.ascii_uppercase[0:9][i] + str(j)
                var = csp.Variable(name, set(range(1, 10)))
                var.neighbors = self.get_neighbor_index_set(i, j)
                if val != 0:
                    var.assigned = val
                    var.final = True
                    var.domain.intersection_update({val})
                self.variables[i, j] = var

    @staticmethod
    def get_neighbor_index_set(i, j):
        rs = i - i % 3
        cs = j - j % 3
        row = [(i, col) for col in range(9) if col != j]
        col = [(row, j) for row in range(9) if row != i]
        box = [(row, col) for row, col in itertools.product(
            range(rs, rs + 3), range(cs, cs + 3)
        ) if row != i and col != j]
        return set(row + col + box)

    def construct_constraints(self):
        row = collections.defaultdict(set)
        col = collections.defaultdict(set)
        box = collections.defaultdict(set)
        for (i, j), var in self.variables.items():
            row[i].add(var)
            col[j].add(var)
            ii = i - i % 3
            jj = j - j % 3
            box[ii, jj].add(var)
        for i, rc in enumerate(row.values()):
            self.constraints.add(csp.AllDiff('R' + str(i), rc))
        for i, cc in enumerate(col.values()):
            self.constraints.add(csp.AllDiff('C' + str(i), cc))
        for i, bc in enumerate(box.values()):
            self.constraints.add(csp.AllDiff('B' + str(i), bc))

    def print_variables(self, color=None):
        if color is None:
            color = 'bold green'
        console = Console()
        s = Text('   | 0 1 2 | 3 4 5 | 6 7 8 ', style='bold white')
        console.print(s)
        console.print(' ' + 25 * '-')
        zero = 0
        for i in range(9):
            a = string.ascii_uppercase[0:9][i]
            t = Text(' ' + a + ' | ', style='bold white')
            for j in range(9):
                var = self.variables[i, j]
                if var.assigned and var.final:
                    t.append(str(var.assigned) + ' ', style=color)
                elif var.assigned:
                    t.append(str(var.assigned) + ' ', style='bold green')
                else:
                    t.append('0 ', style='bold grey')
                    zero += 1
                if j in [2, 5]:
                    t.append('| ')
            console.print(t)
            if i in [2, 5]:
                console.print(' ' + 25 * '-')
        print('Zeros', zero)

    def solve(self):
        self.AC3()
        n = self.assign_single_domains()
        it = 0
        self.print_variables()
        while True:
            print('iteration nr', it)
            self.print_variables()
            na0 = len([var for var in self.variables.values() if var.assigned])
            for con in self.constraints:
                lst = con.eliminate_single()
                if lst:
                    queue = [(Xi, self.variables[i, j]) for Xi in lst for
                             (i, j) in Xi.neighbors]
                    queue2 = [(self.variables[i, j], Xi) for Xi in lst for
                              (i, j) in Xi.neighbors]
                    self.AC3(queue + queue2)
                    n = self.assign_single_domains(n)
            na1 = len([var for var in self.variables.values() if var.assigned])
            it += 1
            if na0 == na1:
                break


        print('SINGLE OVER')
        while True:
            print('iteration nr', it)
            self.print_variables()
            na0 = len([var for var in self.variables.values() if var.assigned])
            for con in self.constraints:
                lst = con.eliminate_double()
                if lst:
                    queue = [(Xi, self.variables[i, j]) for Xi in lst for
                             (i, j) in Xi.neighbors]
                    queue2 = [(self.variables[i, j], Xi) for Xi in lst for
                              (i, j) in Xi.neighbors]
                    self.AC3(queue + queue2)
            n = self.assign_single_domains(n)
            na1 = len([var for var in self.variables.values() if var.assigned])
            it += 1
            if na0 == na1:
                break
        for var in self.variables.values():
            if not var.assigned:
                #print(var.name, var.domain)
                pass

        print('DOUBLE OVER')
        while True:
            print('iteration nr', it)
            self.print_variables()
            na0 = len([var for var in self.variables.values() if var.assigned])
            for con in self.constraints:
                lst = con.eliminate_triple()
                if lst:
                    queue = [(Xi, self.variables[i, j]) for Xi in lst for
                             (i, j) in Xi.neighbors]
                    queue2 = [(self.variables[i, j], Xi) for Xi in lst for
                              (i, j) in Xi.neighbors]
                    self.AC3(queue + queue2)
                    n = self.assign_single_domains(n)
            na1 = len([var for var in self.variables.values() if var.assigned])
            it += 1
            if na0 == na1:
                break



def solve_file():
    with open('sudoku.txt', 'r') as f:
        lines = f.readlines()

    solved = {}
    unsolved = {}

    for i in range(0, len(lines), 10):
        title = lines[i].strip()
        grid0 = [line.strip() for line in lines[i+1:i+10]]
        grid1 = [[int(n) for n in row] for row in grid0]
        sudoku = SudokuCSP(grid1)
        sudoku.solve()
        if sudoku.is_solved():
            solved[title] = sudoku
        else:
            unsolved[title] = sudoku
            


#sudoku = SudokuCSP(zhaw)
sudoku = SudokuCSP(grid10)
#sudoku = SudokuCSP(grid55)
#sudoku = SudokuCSP(aima)
#sudoku.print_variables()
sudoku.solve()
#print('start grid')
#sudoku.print_variables()
#sudoku.solve()
#sudoku.print_variables()


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
