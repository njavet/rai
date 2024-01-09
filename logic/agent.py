from rich.text import Text
from rich.console import Console
import random
import itertools
import functools
import logic
import propkb


class Agent:
    def __init__(self, name):
        self.name = name
        self.performance = 0
        self.location = (0, 0)
        self.direction = 'EAST'
        self.steps = 0
        self.has_arrow = True
        self.kb = propkb.KB()

    def tell_initial_knowledge(self):
        self.kb.tell(logic.Not(logic.Symbol('P00', 'pit is in cell 0,0')))
        self.kb.tell(logic.Not(logic.Symbol('W00', 'wumpus is in cell 0,0')))
        self.kb.tell(logic.Symbol('V00', 'visited cell 0, 0'))

    def turn_left(self):
        self.steps += 1
        if self.direction == 'EAST':
            self.direction = 'NORTH'
        elif self.direction == 'NORTH':
            self.direction = 'WEST'
        elif self.direction == 'WEST':
            self.direction = 'SOUTH'
        elif self.direction == 'SOUTH':
            self.direction = 'EAST'

    def turn_right(self):
        self.steps += 1
        if self.direction == 'EAST':
            self.direction = 'SOUTH'
        elif self.direction == 'NORTH':
            self.direction = 'EAST'
        elif self.direction == 'WEST':
            self.direction = 'NORTH'
        elif self.direction == 'SOUTH':
            self.direction = 'WEST'

    def move_forward(self):
        self.steps += 1
        i, j = self.location
        if self.direction == 'EAST':
            j += 1
        elif self.direction == 'NORTH':
            i += 1
        elif self.direction == 'WEST':
            j -= 1
        elif self.direction == 'SOUTH':
            i -= 1
        self.location = i, j

    def grab_gold(self):
        self.steps += 1

    def shoot(self):
        self.steps += 1
        self.has_arrow = False

    def climb_out(self):
        self.steps += 1
        # moves out of the world
        self.location = -1, -1

    def agent_program(self, percept):
        sentence = self.make_percept_sentence(percept)
        self.kb.tell(sentence)
        query = self.make_action_query()
        if self.kb.ask(query):
            self.move_forward()

    def make_percept_sentence(self, percept):
        def helper(p, s):
            if s not in self.kb.symbols:
                if p:
                    sentence = logic.Symbol(s)
                else:
                    sentence = logic.Not(logic.Symbol(s))
                sentences.append(sentence)

        i, j = self.location
        # visited this cell
        if not self.kb.ask(logic.Symbol('V' + str(i) + str(j))):
            sij = 'S' + str(i) + str(j)
            bij = 'B' + str(i) + str(j)
            gij = 'G' + str(i) + str(j)
            hij = 'H' + str(i) + str(j)
            dij = 'D' + str(i) + str(j)
            sentences = []
            for per, sym in zip(percept, [sij, bij, gij, hij, dij]):
                helper(per, sym)

            return functools.reduce(logic.And, sentences, sentences[0])

    def make_action_query(self):
        i, j = self.location
        query = logic.Symbol('A' + str(i) + str(j))
        return query

