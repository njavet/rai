
from enum import Enum
class Environment:
    def __init__(self):
        self.grid = [[1, 1, 1, 1, 1],
                     [1, 0, 1, 1, 1],
                     [1, 0, 1, 0, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1]]


class State:
    pass


class Reward:
    pass
class Action(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
