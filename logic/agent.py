from rich.text import Text
from rich.console import Console
import random
import itertools
import functools
import logic
import propkb


class Percept:
    """
    kant style: the agent constructs the world :-)
    """
    def __init__(self, row, col, t, stench, breeze, glitter):
        self.row = row
        self.col = col
        self.t = t
        self.stench = stench
        self.breeze = breeze
        self.glitter = glitter

    def make_sentence(self):
        s = logic.create_space_time_prop_var('S', self.row, self.col, self.t)
        b = logic.create_space_time_prop_var('B', self.row, self.col, self.t)
        g = logic.create_space_time_prop_var('G', self.row, self.col, self.t)
        v = logic.create_space_time_prop_var('V', self.row, self.col, self.t)




class Action:
    def __init__(self):
        self.to_left = {
            (1, 0): (0, 1),
            (0, 1): (-1, 0),
            (-1, 0): (0, -1),
            (0, -1): (1, 0)
        }
        self.to_right = {
            (1, 0): (0, -1),
            (0, -1): (-1, 0),
            (-1, 0): (0, 1),
            (0, 1): (1, 0)
        }

    def turn_left(self, fd):
        return self.to_left[fd]

    def turn_right(self, fd):
        return self.to_right[fd]

    def move(self, location, fd):
        # cartesian coordinates vs python list of lists
        i, j = fd
        return location[0] + j, location[1] + i


class Agent:
    def __init__(self, name='Agent'):
        self.name = name
        self.performance = 0
        self.steps = itertools.count()
        self.location = 0, 0
        self.face_direction = (1, 0)
        self.has_arrow = True
        self.action = Action()
        self.kb = propkb.KB()

    def grab_gold(self):
        # TODO
        pass

    def shoot(self):
        # TODO
        self.has_arrow = False

    def climb_out(self):
        # TODO
        # moves out of the world
        pass

    def agent_program(self, percept):
        t = next(self.steps)
        sentence = self.make_percept_sentence(percept, t)
        self.kb.tell(sentence)
        query = self.make_action_query(t)
        action = self.kb.ask(query)
        self.kb.tell(self.make_action_sentence(action, t))

    def make_percept_sentence(self, percept, t):
        pt = Percept(*self.location, t, percept[0], percept[1], percept[2])
        return pt.make_sentence()

    def make_action_query(self, t):
        pass

    def make_action_sentence(self, action, t):
        pass


"""
aima world

"""
logic.PropVar('L_00_0')
logic.PropVar('S_00_0')

percept0 = [None, None, None, None, None]
logic.PropVar('S_01_1')
logic.PropVar('S_10_1')
# move forward
logic.PropVar('L_01_1')

percept1 = [None, 'B', None, None, None]
logic.PropVar('P_02_1') or logic.PropVar('P_11_1')
# moves back
logic.PropVar('L_10')
logic.PropVar('W_20') or lo

