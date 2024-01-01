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
    def __init__(self, name: str, domain: set[int]):
        self.name = name
        self.domain = domain 
        self.neighbors = None
        self.assigned = None
        self.final = False


class Constraint:
    def __init__(self, name: str, variables: set):
        self.name = name
        self.variables = variables


class AllDiff(Constraint):
    def __init__(self, name, variables):
        super().__init__(name, variables)

    def eliminate_single(self):
        lst = []
        dix = collections.defaultdict(int)
        for var in self.variables:
            if not var.assigned:
                for val in var.domain:
                    dix[val] += 1

        for val, count in dix.items():
            if count == 1:
                for var in self.variables:
                    if val in var.domain:
                        var.domain.intersection_update({val})
                        lst.append(var)
        return lst

    def eliminate_double(self):
        lst = []
        nonass = [var for var in self.variables if not var.assigned
                  and len(var.domain) == 2]
        n1 = [var for var in self.variables if not var.assigned]
        for var in nonass:
            for var2 in nonass:
                if var2.name != var.name and var2.domain == var.domain:
                    others = [v for v in n1
                                if v.name != var.name and v.name != var2.name]
                    for v in others:
                        v.domain.difference_update(var.domain)
                        lst.append(v)
                        print('updated double',
                                  self.name,
                                    v.name, v.domain,
                                  var.name, var.domain,
                                  var2.name, var2.domain)
        return lst

    def eliminate_triple(self):
        lst = []
        nonass = [var for var in self.variables if not var.assigned
                  and len(var.domain) <= 3]

        for var in nonass:
            names = [var.name]
            for var2 in nonass:
                if var2.name not in names and var2.domain.issubset(var.domain):
                    names.append(var2.name)
                    for var3 in nonass:
                        if var3.name not in names:
                            if var3.domain.issubset(var.domain) and var3.domain.issubset(var2.domain):
                                others = [v for v in self.variables if v.name not in names]
                                for v in others:
                                    print('updated triple',
                                        self.name,
                                  var.name, var.domain,
                                  var2.name, var2.domain)
                                    v.domain.difference_update(var.domain)
                                    lst.append(v)
        return lst







class CSP:
    def __init__(self):
        self.variables: dict = {}
        self.constraints = set()

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
                    # Xj, Xi is added too
                    Xk = self.variables[i, j]
                    if Xk.name != Xj.name:
                        queue.append((Xk, Xi))
        return True

    def assign_single_domains(self, nassigned=0):
        for var in self.variables.values():
            if not var.assigned and len(var.domain) == 1:
                nassigned += 1
                var.assigned = var.domain.copy().pop()
                var.final = True
        return nassigned


