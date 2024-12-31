
# project imports
from rai.rl.envs.base import BaseEnv


class Grid(BaseEnv):
    def __init__(self, m: int = 5, n: int = 5):
        super().__init__('grid')
        self.m = m
        self.n = n

    def reset(self) -> tuple[int, str]:
        self.agent_pos = 0
        return self.agent_pos, 'No info yet'

    def pos_to_tuple(self):
        """ convert integer position to grid position"""
        x, y = divmod(self.agent_pos, self.m)
        return x, y

    def update_agent_position(self, x, y):
        self.agent_pos = x * self.m + y

    @staticmethod
    def get_action_values(action):
        if action.value == 0:
            return 0, -1
        elif action.value == 1:
            return 1, 0
        elif action.value == 2:
            return 0, 1
        elif action.value == 3:
            return -1, 0
        raise ValueError('invalid action')

    def step(self, action):
        x, y = self.pos_to_tuple()
        ax, ay = self.get_action_values(action)
        x1 = max(x + ax, 0)
        y1 = max(y + ay, 0)
        x_new = min(x1, self.m - 1)
        y_new = min(y1, self.n - 1)
        self.update_agent_position(x_new, y_new)

        state = x_new, y_new
        reward = -1
        is_terminal = self.agent_pos == self.goal_pos
        return state, reward, is_terminal, False, None
