import logging
import string
import collections
import itertools
from rich.console import Console
from rich.text import Text

import csp
"""
least constraining value:
isn't it better (at least for sudoku) to take the value that
rules out the most values in the remaining variables ? because
then either we fail faster and can move on, or we find the (unique)
solution faster ?

AC3 is constraint propagation, while
forward checking would only look at the neighbors of the current
variable 
"""


class Sudoku(csp.CSP):
    def __init__(self, grid):
        super().__init__()
        self.construct_variables(grid)
        self.construct_constraints()
        self.ass = None

    def construct_variables(self, grid):
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                name = string.ascii_uppercase[0:9][i] + str(j)
                self.variables.add(name)
                if val == 0:
                    self.domains[name] = set(range(1, 10))
                else:
                    self.domains[name] = {val}
                self.neighbors[name] = self.get_neighbors(i, j)

    @staticmethod
    def get_neighbors(i, j):
        rs = i - i % 3
        cs = j - j % 3
        row = [(i, col) for col in range(9) if col != j]
        col = [(row, j) for row in range(9) if row != i]
        box = [(row, col) for row, col in itertools.product(
            range(rs, rs + 3), range(cs, cs + 3)
        ) if row != i and col != j]
        indexes = set(row + col + box)
        return {string.ascii_uppercase[0:9][ii] + str(jj) for ii, jj in indexes}

    def construct_constraints(self):
        rows = collections.defaultdict(list)
        cols = collections.defaultdict(list)
        for c, d in itertools.product(string.ascii_uppercase[0:9], string.digits[0:9]):
            rows[c].append(c + d)
            cols[d].append(c + d)
        row_sets = [set(row) for row in rows.values()]
        col_sets = [set(col) for col in cols.values()]
        for i in range(3):
            ru = self.append_and_union(i, row_sets)
            for j in range(3):
                cu = self.append_and_union(j, col_sets)
                self.constraints.append(ru.intersection(cu))

    def append_and_union(self, ind, sets):
        s0 = sets[3 * ind]
        self.constraints.append(s0)
        s1 = sets[3 * ind + 1]
        self.constraints.append(s1)
        s2 = sets[3 * ind + 2]
        self.constraints.append(s2)
        return s0.union(s1).union(s2)

    @staticmethod
    def print_grid(assignments):
        console = Console()
        s = Text('   | 0 1 2 | 3 4 5 | 6 7 8 ', style='bold white')
        console.print(s)
        console.print(' ' + 25 * '-')
        zero = 0
        for i in range(9):
            a = string.ascii_uppercase[0:9][i]
            t = Text(' ' + a + ' | ', style='bold white')
            for j in range(9):
                name = string.ascii_uppercase[0:9][i] + str(j)
                try:
                    val = assignments[name]
                except KeyError:
                    zero += 1
                    val = 0
                t.append(str(val) + ' ', style='bold green')
                if j in [2, 5]:
                    t.append('| ')
            console.print(t)
            if i in [2, 5]:
                console.print(' ' + 25 * '-')
        print('Zeros', zero)

    def to_grid(self, assignments):
        grid = []
        for i in range(9):
            row = []
            a = string.ascii_uppercase[0:9][i]
            for j in range(9):
                name = string.ascii_uppercase[0:9][i] + str(j)
                try:
                    val = assignments[name]
                except KeyError:
                    val = 0
                row.append(val)
            grid.append(row)
        return grid

    def solve(self):
        assignments = {}
        for var in sorted(self.variables):
            if len(self.domains[var]) == 1:
                assignments[var] = list(self.domains[var])[0]
        #self.print_grid(assignments)
        #assignments = {}
        self.AC3()
        self.path = {}
        for var in sorted(self.variables):
            if len(self.domains[var]) > 1:
                self.path[var] = {}
                logging.debug(var + '\t' + ' '.join([str(val) for val in self.domains[var]]))

        self.backtrack_search(assignments)
        self.ass = assignments
        #self.print_grid(assignments)
