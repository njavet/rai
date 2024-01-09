from rich.text import Text
from rich.console import Console
import random
import itertools
import functools
import logic
import propkb


class Agent:
    def __init__(self, name='Agent'):
        self.name = name
        self.performance = 0
        self.location = (0, 0)
        self.direction = 'EAST'
        self.steps = itertools.count()
        self.has_arrow = True
        self.kb = propkb.KB()

    def turn_left(self):
        if self.direction == 'EAST':
            self.direction = 'NORTH'
        elif self.direction == 'NORTH':
            self.direction = 'WEST'
        elif self.direction == 'WEST':
            self.direction = 'SOUTH'
        elif self.direction == 'SOUTH':
            self.direction = 'EAST'

    def turn_right(self):
        if self.direction == 'EAST':
            self.direction = 'SOUTH'
        elif self.direction == 'NORTH':
            self.direction = 'EAST'
        elif self.direction == 'WEST':
            self.direction = 'NORTH'
        elif self.direction == 'SOUTH':
            self.direction = 'WEST'

    def move_forward(self):
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
        # TODO
        pass

    def shoot(self):
        # TODO
        self.has_arrow = False

    def climb_out(self):
        # TODO
        # moves out of the world
        self.location = -1, -1

    def agent_program(self, percept):
        t = next(self.steps)
        sentence = self.make_percept_sentence(percept, t)
        self.kb.tell(sentence)
        query = self.make_action_query(t)
        action = self.kb.ask(query)
        if action == 0:
            self.turn_left()
        if action == 1:
            self.turn_right()
        if action == 2:
            self.move_forward()

        #self.kb.tell(self.make_action_sentence(action, t))
        return action

    def make_percept_sentence(self, percept, t):
        sentences = []
        def helper(p, s):
            if p:
                sentence = logic.Symbol(s)
            else:
                sentence = logic.Not(logic.Symbol(s))
            sentences.append(sentence)

        i, j = self.location

        pinf = logic.And(logic.Symbol('V' + str(i) + str(j)),
                         logic.Symbol(self.direction + str(i) + str(j)))
        sij = 'S' + str(i) + str(j)
        bij = 'B' + str(i) + str(j)
        gij = 'G' + str(i) + str(j)
        hij = 'H' + str(i) + str(j)
        dij = 'D' + str(i) + str(j)
        sentences = []
        for per, sym in zip(percept, [sij, bij, gij, hij, dij]):
            helper(per, sym)
        return functools.reduce(logic.And, sentences, pinf)

    def make_action_query(self, t):
        i, j = self.location
        query = logic.Symbol('M' + str(i) + str(j))
        return query

    def make_action_sentence(self, action, t):
        i, j = self.location
        return logic.Symbol('M' + str(i) + str(j))

