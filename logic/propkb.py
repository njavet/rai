import functools

from rich.text import Text
from rich.console import Console
import random
import itertools

import logic
# standard logical equivalences
# (A ∧ B) ≡ (B ∧ A) commutativity of ∧
# (A ∨ B) ≡ (B ∨ A) commutativity of ∨
# ((A ∧ B) ∧ C) ≡ (A ∧ (B ∧ C)) associativity of ∧
# ((A ∨ B) ∨ C) ≡ (A ∨ (B ∨ C)) associativity of ∨
# ¬(¬A) ≡ A double negation elimination


p00 = '(((A ∨ B) → C) ∧ (D ∧ (¬E)))'


class KB:
    def __init__(self):
        self.model = {}
        self.sentences = []
        self.initial_knowledge()

    def initial_knowledge(self):
        self.sentences.append(logic.Not(logic.Symbol('P00')))
        self.sentences.append(logic.Not(logic.Symbol('W00')))
        self.model['P00'] = False
        self.model['W00'] = False

    def tell(self, sentence):
        for literal in sentence.get_literal_list():
            if isinstance(literal, logic.Not):
                litsym = literal.get_symbol_list()[0]
                if litsym not in self.model.keys():
                    self.model[litsym] = False
            else:
                litsym = literal.symbol
                # breeze
                if litsym.startswith('B'):
                    clause = self.breeze(litsym)
                    sentence = logic.And(sentence, clause)
                # stench
                if litsym.startswith('S'):
                    clause = self.stench(litsym)
                    sentence = logic.And(sentence, clause)
                if litsym not in self.model.keys():
                    self.model[literal.symbol] = True
        self.sentences.append(sentence)

    def ask(self, sentence):
        kb = functools.reduce(logic.And, self.sentences[1:], self.sentences[0])
        syms = self.sentences[-1].get_symbol_list()
        no_move = False
        turn = 'left'
        for sym in syms:
            if sym.startswith('V'):
                i, j = int(sym[1]), int(sym[2])

        new_i, new_j = -1, -1
        for sym in syms:
            if sym.startswith('EAST'):
                if j == 3:
                    no_move = True
                else:
                    new_i = i
                    new_j = j + 1

            if sym.startswith('NORTH'):
                if i == 0:
                    no_move = True
                else:
                    new_i = i - 1
                    new_j = j
            if sym.startswith('WEST'):
                if j == 0:
                    no_move = True
                else:
                    new_i = i
                    new_j = j - 1
            if sym.startswith('SOUTH'):
                if i == 3:
                    no_move = True
                else:
                    new_i = i + 1
                    new_j = j
        if not no_move:
            isp = logic.Not(logic.Symbol('P' + str(new_i) + str(new_j)))
            isw = logic.Not(logic.Symbol('W' + str(new_i) + str(new_j)))
            if logic.tt_entails(kb, logic.And(isp, isw)):
                return 2
        else:
            return 1

        #print('kb', kb, 'sentence', sentence, 'res', res)
        return logic.tt_entails(kb, sentence)

    def breeze(self, litsym):
        i, j = int(litsym[1]), int(litsym[2])
        inds = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
        danger = []
        for ii, jj in inds:
            if ii in [0, 1, 2, 3] and jj in [0, 1, 2, 3]:
                d = logic.Symbol('P' + str(ii) + str(jj))
                if 'P' + str(ii) + str(jj) in self.model.keys():
                    d = logic.Not(d)
                danger.append(d)
        return functools.reduce(logic.Or, danger[1:], danger[0])

    def stench(self, litsym):
        i, j = int(litsym[1]), int(litsym[2])
        inds = [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)]
        danger = []
        for ii, jj in inds:
            if ii in [0, 1, 2, 3] and jj in [0, 1, 2, 3]:
                d = logic.Symbol('W' + str(ii) + str(jj))
                if 'W' + str(ii) + str(jj) in self.model.keys():
                    d = logic.Not(d)
                danger.append(d)
        return functools.reduce(logic.Or, danger[1:], danger[0])

    def inference(self):
        pass


