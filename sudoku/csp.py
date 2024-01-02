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
        self.variables = None
        self.domains = None
        self.simdoms = None
        self.neighbors = None
        self.n_bt = 0

    def select_unassigned_variable(self, mode):
        # greedy
        if mode == 'greedy':
            for var in self.variables:
                if not var.assigned:
                    return var
        elif mode == 'mrv':
            pass


    @staticmethod
    def _revise(Xi, Xj):
        revised = False
        for x in list(Xi.domain):
            if all([x == y for y in Xj.domain]):
                Xi.domain.remove(x)
                revised = True
        return revised

    def AC3(self, queue=None):
        if queue is None:
            queue = [(Xi, self.variables[i, j])
                     for Xi in self.variables.values()
                     for (i, j) in Xi.neighbors]
        while queue:
            Xi, Xj = queue.pop()
            if self._revise(Xi, Xj):
                if len(Xi.domain) == 0:
                    return False
                for (i, j) in Xi.neighbors:
                    Xk = self.variables[i, j]
                    if Xk.name != Xj.name:
                        queue.append((Xk, Xi))
        return True

    def assign_single_value_domains(self, nassigned=0):
        for var in self.variables.values():
            if not var.assigned and len(var.domain) == 1:
                nassigned += 1
                var.assigned = var.domain.copy().pop()
        return nassigned


