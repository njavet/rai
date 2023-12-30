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
        # step is only for rich color printing 
        # when it was assigned
        self.name = name
        self.domain = domain 
        self.assigned = None
        self.step = 0
        self.neighbors = None


class Constraint:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables


class AllDiff(Constraint):
    def __init__(self, name, variables):
        super().__init__(name, variables)

    def reduce_constraint_variables_domain(self):
        print('checking ', self.name)
        lst = []
        dix = collections.defaultdict(int)
        for var in self.variables:
            if not var.assigned:
                for val in var.domain:
                    dix[val] += 1

        for val, count in dix.items():
            if count == 1:
                for var in self.variables:
                    print('\tvar:', var.domain)
                    if val in var.domain:
                        var.domain = [val]
                        lst.append(var)
                        print('\tdomain reduced: ', var.name, var.domain)
        return lst

    def is_partial_solution(self):
        lst = []
        for var in self.variables:
            if var.assigned:
                lst.assigned.append(var.assigned)
        # all values are different
        return len(set(lst)) == len(lst)

    def is_solution(self):
        nvars = len(self.variables)
        con1 = len(lst) == nvars
        return con1 and self.is_partial_solution()


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

    def AC3(self, queue=None):
        """ arc constraints makes only sense with len(Xj.domain) == 1 ? 
            since it only looks at a pair of variables. if len(Xj.domain) > 1
            we obviously can just compare the seconds number, which is not equal
            to the first one
        """
        if queue is None:
            queue = [(Xi, Xj) for Xi in self.variables.values() for Xj in Xi.neighbors]
        rev = 0
        while queue:
            Xi, Xj = queue.pop()
            if self._revise(Xi, Xj):
                rev += 1
                if len(Xi.domain) == 0:
                    return False
                for Xk in [Xn for Xn in Xi.neighbors if Xn.name != Xj.name]:
                    queue.append((Xk, Xi))
        print('revised', rev)
        return True


