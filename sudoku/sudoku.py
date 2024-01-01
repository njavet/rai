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
        self.steps = 0

    def construct_variables(self, grid):
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                name = string.ascii_uppercase[0:9][i] + str(j)
                var = csp.Variable(name, set(range(1, 10)))
                var.neighbors = self.get_neighbor_index_set(i, j)
                if val != 0:
                    var.assigned = val
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

    def print_grid(self, color=None):
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
                if var.assigned:
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

    def print_variables(self):
        for (i, j), var in self.variables.items():
            print(var.name, var.domain)

    def mrv(self):
        pass

    def backtrack_search(self):
        var = self.select_unassigned_variable()
        if var is None:
            return True

        for val in var.domain:
            var.assigned = val
            queue0 = [(var, self.variables[i, j]) for (i, j) in var.neighbors]
            queue1 = [(self.variables[i, j], var) for (i, j) in var.neighbors]
            if not self.AC3(queue0 + queue1):
                # revert to the domains before trying this solution
                for v in self.variables.values():
                    v.domain = v.domain_copy.copy()
                return False
            if self.backtrack_search():
                return True
            var.assigned = None

    def solve(self):
        pass




