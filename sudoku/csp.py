import string
import collections

"""
a constraint satisfaction problem consists of three components:
    X: set of variables
    D:  set of domains, one for each variable
    C: constraints that specify allowable combinations of values


assignment: a : X -> D*

"""


class CSP:
    def __init__(self):
        self.variables = set()
        # str: set
        self.domains = dict()
        # str: set
        self.neighbors = dict()
        self.constraints = []
        self.n_bt = 0
        self.n_ass = 0

    def select_unassigned_variable(self, assignments, mode):
        unassigned = self.variables.difference(set(assignments.keys()))
        # greedy
        if mode == 'greedy':
            try:
                var = unassigned.pop()
            except TypeError:
                var = None
        elif mode == 'mrv':
            try:
                var = sorted(unassigned, key=lambda v: len(self.domains[v]))[0]
            except IndexError:
                var = None
        return var

    def _revise(self, var_i, var_j):
        revised = []
        for x in list(self.domains[var_i]):
            if all([x == y for y in self.domains[var_j]]):
                self.domains[var_i].remove(x)
                revised.append((var_i, x))
        return revised

    def AC3(self, queue=None):
        if queue is None:
            queue = [(x, y) for x in self.variables for y in self.neighbors[x]]
        revised = []
        while queue:
            x, y = queue.pop()
            rev = self._revise(x, y)
            if rev:
                revised = revised + rev
                if len(self.domains[x]) == 0:
                    return False, revised
                for z in self.neighbors[x]:
                    if z != y:
                        queue.append((z, x))
        return True, revised

    def mac(self, var):
        q0 = [(var, x) for x in self.neighbors[var]]
        q1 = [(x, var) for x in self.neighbors[var]]
        return self.AC3(q0 + q1)

    def nconflicts(self, var, val, assignments):
        count = 0
        for var2 in self.neighbors[var]:
            try:
                val2 = assignments[var2]
                if val == val2:
                    count += 1
            except KeyError:
                pass
        return count

    def restore(self, revised):
        for var, val in revised:
            self.domains[var].add(val)

    def backtrack_search(self, assignments):
        self.n_bt += 1
        var = self.select_unassigned_variable(assignments, 'mrv')
        if var is None:
            return True

        for val in self.domains[var]:
            if 0 == self.nconflicts(var, val, assignments):
                # assign
                assignments[var] = val
                self.n_ass += 1
                inf, revised = self.mac(var)
                if inf:
                    if self.backtrack_search(assignments):
                        return True
                self.restore(revised)
        try:
            del assignments[var]
        except KeyError:
            pass
