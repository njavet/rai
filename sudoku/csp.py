import string
import collections

"""
a constraint satisfaction problem consists of three components:
    X: set of variables
    D:  set of domains, one for each variable
    C: constraints that specify allowable combinations of values


assignment: a : X -> D*

"""


class Variable:
    def __init__(self, name: str, domain: list[int]):
        self.name = name
        self.domain = domain 
        self.assigned = None
        self.neighbors = None


class Constraint:
    def __init__(self, variables):
        self.variables = variables


class AllDiff(Constraint):
    def __init__(self, variables):
        super().__init__(variables)

    def prune(self):
        dix = collections.defaultdict(int)
        for var in self.variables:
            for val in var.domain:
                dix[val] += 1

        for val, count in dix.items():
            if count == 1:
                for var in self.variables:
                    if val in var.domain:
                        var.assigned = val
                        ind = var.domain.index(val)
                        del var.domain[ind]
                        print('pruned ', var.name, val)
                        return True
        return False

    def satisfied(self):
        lst = []
        for var in self.variables:
            if var.assigned:
                lst.assigned.append(var.assigned)
        return len(set(lst)) == len(lst)


class CSP:
    def __init__(self):
        self.variables = None
        self.constraints = None

    def _revise(self, Xi, Xj):
        revised = False
        for i, x in enumerate(Xi.domain):
            if all([x == y for y in Xj.domain]):
                del Xi.domain[i]
                revised = True
        return revised

    def AC3(self, queue):
        """ arc constraints makes only sense with len(Xj.domain) == 1 ? 
            since it only looks at a pair of variables. if len(Xj.domain) > 1
            we obviously can just compare the seconds number, which is not equal
            to the first one
        """
        while queue:
            Xi, Xj = queue.pop()
            if self._revise(Xi, Xj):
                if len(Xi.domain) == 0:
                    return False
                for Xk in [Xn for Xn in Xi.neighbors if Xn.name != Xj.name]:
                    queue.append((Xk, Xi))
        return True


