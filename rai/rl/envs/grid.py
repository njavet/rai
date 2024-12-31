
# project imports
from rai.rl.models import Action


class Grid:
    def __init__(self, height: int = 5, width: int = 5):
        self.height = height
        self.width = width
        self.cur_pos = 0, 0
        self.goal = self.height - 1, self.width - 1

    def reset(self):
        self.cur_pos = 0, 0
        return (0, 0), 0, False

    @staticmethod
    def get_action_values(action: Action):
        if action.value == 0:
            return 0, -1
        elif action.value == 1:
            return 1, 0
        elif action.value == 2:
            return 0, 1
        elif action.value == 3:
            return -1, 0
        raise ValueError('invalid action')

    def step(self, action: Action):
        x, y = self.cur_pos[0], self.cur_pos[1]
        ax, ay = self.get_action_values(action)
        x1 = max(x + ax, 0)
        y1 = max(y + ay, 0)
        x_new = min(x1, self.width-1)
        y_new = min(y1, self.height-1)
        self.cur_pos = x_new, y_new
        state = x_new, y_new
        reward = -1
        is_terminal = self.cur_pos == self.goal
        return state, reward, is_terminal
