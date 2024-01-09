import functools
from string import ascii_uppercase


class Sentence:
    def __init__(self):
        self.is_literal = False
        self.is_clause = False
        self.is_cnf = False

    """ well-formed formula"""
    def evaluate(self, model):
        pass

    def is_atomic(self):
        return isinstance(self, Symbol)

    def is_negation(self):
        return isinstance(self, Not)

    def get_symbol_list(self):
        pass

    def get_literal_list(self):
        pass


class Symbol(Sentence):
    """ proposition variable"""
    def __init__(self, symbol, description=None):
        super().__init__()
        self.is_literal = True
        self.is_clause = True
        self.is_cnf = True
        self.symbol = symbol
        self.description = description

    def __str__(self):
        return self.symbol

    def evaluate(self, model):
        # should it be True or False if the model does not assign the Symbol ?
        return model.get(self.symbol, False)

    def get_symbol_list(self):
        return [self.symbol]

    def get_literal_list(self):
        return [self]


class Not(Sentence):
    def __init__(self, proposition: Sentence):
        super().__init__()
        if proposition.is_literal:
            self.is_literal = True
            self.is_clause = True
            self.is_cnf = True
        self.proposition = proposition

    def __str__(self):
        if self.proposition.is_atomic():
            return '¬' + str(self.proposition)
        else:
            return '¬(' + str(self.proposition) + ')'

    def evaluate(self, model):
        return not self.proposition.evaluate(model)

    def get_symbol_list(self):
        return self.proposition.get_symbol_list()

    def get_literal_list(self):
        return [self]


class Implication(Sentence):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def __str__(self):
        return '(' + str(self.left) + ' → ' + str(self.right) + ')'

    def evaluate(self, model):
        return not self.left.evaluate(model) or self.right.evaluate(model)

    def get_symbol_list(self):
        return self.left.get_symbol_list() + self.right.get_symbol_list()

    def get_literal_list(self):
        return self.left.get_literal_list() + self.right.get_literal_list()

class And(Sentence):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        if self.left.is_clause and self.right.is_clause:
            self.is_cnf = True

    def __str__(self):
        return '(' + str(self.left) + ' ∧ ' + str(self.right) + ')'

    def evaluate(self, model):
        return self.left.evaluate(model) and self.right.evaluate(model)

    def get_symbol_list(self):
        return self.left.get_symbol_list() + self.right.get_symbol_list()

    def get_literal_list(self):
        return self.left.get_literal_list() + self.right.get_literal_list()


class Or(Sentence):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        if self.left.is_literal and self.right.is_literal:
            self.is_clause = True

    def __str__(self):
        return '(' + str(self.left) + ' ∨ ' + str(self.right) + ')'

    def evaluate(self, model):
        return self.left.evaluate(model) or self.right.evaluate(model)

    def get_symbol_list(self):
        return self.left.get_symbol_list() + self.right.get_symbol_list()

    def get_literal_list(self):
        return self.left.get_literal_list() + self.right.get_literal_list()


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


def pl_true(s: Sentence, model):
    return s.evaluate(model)



