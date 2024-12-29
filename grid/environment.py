from enum import Enum
from pydantic import BaseModel
from itertools import product


class Action(Enum):
    # finite set of actions
    UP = -1, 0
    RIGHT = 0, 1
    DOWN = 1, 0
    LEFT = 0, -1


class State(BaseModel):
    x: int
    y: int
    goal: bool = False
    curr: bool = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        if self.goal:
            return 'T'
        elif self.curr:
            return 'X'
        else:
            return ' '


class Grid:
    def __init__(self, height: int = 5, width: int = 5):
        self.height = height
        self.width = width
        self.grid = self.construct_grid()
        self.cur_pos = self.grid[(0, 0)]
        self.goal = self.grid[(self.height-1, self.width-1)]

    def construct_grid(self):
        gen = product(range(self.height), range(self.width))
        g = {(x, y): State(x=x, y=y) for x, y in gen}
        g[(0, 0)].curr = True
        g[(self.height-1, self.width-1)].goal = True
        return g

    def reset(self):
        gen = product(range(self.height), range(self.width))
        g = {(x, y): State(x=x, y=y) for x, y in gen}
        g[(0, 0)].curr = True
        g[(self.height-1, self.width-1)].goal = True
        return self.grid[(0, 0)], 0, False

    def step(self, action: Action):
        x, y = self.cur_pos.x, self.cur_pos.y
        self.grid[(x, y)].curr = False
        x1 = max(x + action.value[0], 0)
        y1 = max(y + action.value[1], 0)
        self.cur_pos.x = min(x1, self.width-1)
        self.cur_pos.y = min(y1, self.height-1)

        state = self.grid[(self.cur_pos.x, self.cur_pos.y)]
        state.curr = True
        reward = -1
        is_terminal = self.cur_pos == self.goal
        return state, reward, is_terminal
