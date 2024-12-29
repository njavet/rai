from enum import Enum
from pydantic import BaseModel


class Action(Enum):
    # finite set of actions
    UP = -1, 0
    RIGHT = 0, 1
    DOWN = 1, 0
    LEFT = 0, -1


class Point(BaseModel):
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Grid:
    def __init__(self, height: int = 5, width: int = 5):
        self.height = height
        self.width = width
        self.goal = Point(x=self.width-1, y=self.height-1)
        self.cur_pos = Point(x=0, y=0)

    def reset(self):
        self.cur_pos.x = 0
        self.cur_pos.y = 0
        state = Point(x=self.cur_pos.x, y=self.cur_pos.y)
        return state, 0, False

    def step(self, action: Action):
        x, y = self.cur_pos.x, self.cur_pos.y
        x1 = max(x + action.value[0], 0)
        y1 = max(y + action.value[1], 0)
        self.cur_pos.x = min(x1, self.width-1)
        self.cur_pos.y = min(y1, self.height-1)

        state = Point(x=self.cur_pos.x, y=self.cur_pos.y)
        reward = -1
        is_terminal = self.cur_pos == self.goal
        return state, reward, is_terminal

    def __repr__(self):
        hsep = self.width * 3 * '-' + 6 * '-'
        res = hsep
        for x in range(self.height):
            res += '\n|'
            for y in range(self.width):
                if self.cur_pos.x == x and self.cur_pos.y == y:
                    res += ' x |'
                elif self.goal.x == x and self.goal.y == y:
                    res += ' T |'
                else:
                    res += '   |'
            res += '\n'
            res += hsep
        return res
