from enum import Enum
from rich.console import Console
from rich.text import Text
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


class TrajectoryElement(BaseModel):
    state: Point
    reward: float
    action: Action | None


class Trajectory(BaseModel):
    elements: tuple[TrajectoryElement]


class Grid:
    def __init__(self, height: int = 5, width: int = 5):
        self.height = height
        self.width = width
        self.goal = Point(x=self.width-1, y=self.height-1)
        self.cur_pos = Point(x=0, y=0)
        self.console = Console()

    def reset(self):
        self.goal = Point(x=self.width-1, y=self.height-1)
        self.cur_pos = Point(x=0, y=0)

    def step(self, action: Action):
        x, y = self.cur_pos.x, self.cur_pos.y
        x1 = max(x + action.value[0], 0)
        y1 = max(y + action.value[1], 0)
        self.cur_pos.x = min(x1, self.width-1)
        self.cur_pos.y = min(y1, self.height-1)

        is_terminal = self.cur_pos == self.goal
        reward = -1
        return self.cur_pos, reward, is_terminal

    def __repr__(self):
        hsep = self.width * 3 * '-' + 6 * '-'
        self.console.print('\n' + hsep, style='cyan')
        for y in range(self.height):
            line = '|'
            for x in range(self.width):
                if self.cur_pos.x == x and self.cur_pos.y == y:
                    line += ' x |'
                elif self.goal.x == x and self.goal.y == y:
                    line += ' T |'
                else:
                    line += '   |'

            self.console.print(line, style='cyan')
            self.console.print(hsep, style='cyan')
