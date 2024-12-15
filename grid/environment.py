from enum import Enum


class Environment:
    def __init__(self):
        self.grid = [[1, 1, 1, 1, 1],
                     [1, 0, 1, 1, 1],
                     [1, 0, 1, 0, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1]]
        self.state = State(3, 0)


class State:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return self.x, self.y


class Reward:
    def __init__(self):
        self.r = -1


class Action(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
