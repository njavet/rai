import gymnasium as gym

# project imports
from rai.rl.models.base import BaseGridModel


class FLModel(BaseGridModel):
    def __init__(self, m: int, n: int, env: gym.Env) -> None:
        super().__init__(m, n)
        self.env = env
        self.terminal_state = None

    def reset(self,
              *,
              seed: int | None = None,
              options: dict[str, Any] | None = None
              ) -> tuple[ObsType, dict[str, Any]]:
        self.steps = 0
        self.state = 0
        return self.state, {'start': 0}

    def pos_to_tuple(self):
        """ convert integer position to grid position"""
        x, y = divmod(self.state, self.m)
        return x, y

    def update_agent_position(self, ax, ay):
        x, y = self.pos_to_tuple()
        x1 = max(x + ax, 0)
        y1 = max(y + ay, 0)
        x_new = min(x1, self.m - 1)
        y_new = min(y1, self.n - 1)
        self.agent_pos = x_new * self.m + y_new

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

    @staticmethod
    def reward_table(state, next_state):
        if state == next_state:
            return -0.5
        elif (state, next_state) in [(0, 1),
                                     (1, 2),
                                     (2, 3),
                                     (3, 7),
                                     (7, 11),
                                     (11, 10),
                                     (10, 9),
                                     (9, 8),
                                     (8, 4),
                                     (4, 5),
                                     (5, 6),
                                     (6, 7),
                                     (11, 15)]:
            return 1
        else:
            return 0

    def step(self, action):
        self.steps += 1
        ax, ay = self.get_action_values(action)
        state = self.agent_pos
        self.update_agent_position(ax, ay)
        next_state = self.agent_pos
        reward = self.reward_table(state, next_state)
        is_terminal = self.agent_pos == self.term
        trunc = self.steps >= self.max_steps
        return self.agent_pos, reward, is_terminal, trunc, None
