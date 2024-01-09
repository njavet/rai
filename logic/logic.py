

class WFF:
    """ well-formed formula"""
    def evaluate(self, model):
        pass

    def is_atomic(self):
        return isinstance(self, PropVar)


class PropVar(WFF):
    """ proposition variable"""
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def evaluate(self, model):
        # should it be True or False if the model does not assign the Symbol ?
        return model.get(self.name, False)


class Not(WFF):
    def __init__(self, wff: WFF):
        self.wff = wff

    def __str__(self):
        if self.wff.is_atomic():
            return '¬' + str(self.wff)
        else:
            return '¬(' + str(self.wff) + ')'

    @classmethod
    def from_prop_var(cls, name):
        return cls(PropVar(name))

    def evaluate(self, model):
        return not self.wff.evaluate(model)


class Implication(WFF):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '(' + str(self.left) + ' → ' + str(self.right) + ')'

    @classmethod
    def from_prop_vars(cls, name0, name1):
        p0 = PropVar(name0)
        p1 = PropVar(name1)
        return cls(p0, p1)

    def evaluate(self, model):
        return not self.left.evaluate(model) or self.right.evaluate(model)


class And(WFF):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return '(' + str(self.left) + ' ∧ ' + str(self.right) + ')'

    @classmethod
    def from_prop_vars(cls, name0, name1):
        p0 = PropVar(name0)
        p1 = PropVar(name1)
        return cls(p0, p1)

    def evaluate(self, model):
        return self.left.evaluate(model) and self.right.evaluate(model)


class Or(WFF):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return '(' + str(self.left) + ' ∨ ' + str(self.right) + ')'

    @classmethod
    def from_prop_vars(cls, name0, name1):
        p0 = PropVar(name0)
        p1 = PropVar(name1)
        return cls(p0, p1)

    def evaluate(self, model):
        return self.left.evaluate(model) or self.right.evaluate(model)


def tt_entails(kb, alpha):
    symbols = kb.get_symbol_list() + alpha.get_symbol_list()
    return tt_check_all(kb, alpha, symbols, {})


def tt_check_all(kb, alpha, symbols, model):
    if not symbols:
        if pl_true(kb, model):
            return pl_true(alpha, model)
        else:
            return True
    p = symbols.pop()
    cond0 = tt_check_all(kb, alpha, symbols, model | {p: True})
    cond1 = tt_check_all(kb, alpha, symbols, model | {p: False})
    return cond0 and cond1


def pl_true(s: WFF, model):
    return s.evaluate(model)


def create_space_time_prop_var(name, row, col, t):
    vname = name + '_' + str(row) + str(col) + '_' + str(t)
    return PropVar(vname)

# lab03
# A: unicorn is mythical
# B: unicorn is immortal
# C: unicorn is a mortal mammal
# D: unicorn is a mammal
# E: unicorn is horned
# F: unicorn is magical
# (A -> B) ∧ (¬A -> C)
# (B ∨ ∧ (¬A -> C)
# (B ∨ D) -> E
# E -> F

## wumpus axtioms

# no pit in 0, 0
axiom00 = Not.from_prop_var('P00')
# no wumpus in 0, 0
axiom01 = Not.from_prop_var('W00')
# start location == 0, 0
axiom02 = PropVar('L00')

