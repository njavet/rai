import gymnasium as gym
from gymnasium.core import RenderFrame
from gymnasium.spaces import Discrete


class DungeonEnv(gym.Env):
    def __init__(self):
        self.action_space = Discrete(4)
        self.observation_space = Discrete(16)
        self.agent_position = 0
        self.gpu_position = 15
        self.pits = [3, 5, 10, 12, 14]
        self.steps = 0
        self.has_gpu = False

    def reset(self):
        self.steps = 0
        self.agent_position = 0
        self.has_gpu = False
        return 0, 'start position'

    def render(self) -> RenderFrame | list[RenderFrame] | None:
        grid = [['0', '0', '0', '1'],
                ['0', '1', '0', '0'],
                ['0', '0', '1', '0'],
                ['1', '0', '1', 'G']]
        a, b = divmod(self.agent_position, 4)
        grid[a][b] = 'A'
        print(grid)

    def step(self, action):
        reward = -0.5

        term = False
        if action == 0:
            if self.agent_position not in [0, 4, 8, 12]:
                self.agent_position -= 1
        elif action == 1:
            if self.agent_position < 12:
                self.agent_position += 4
        elif action == 2:
            if self.agent_position not in [3, 7, 11, 15]:
                self.agent_position += 1
        elif action == 3:
            if self.agent_position not in range(4):
                self.agent_position -= 4
        if self.agent_position in self.pits:
            term = True
            reward -= 10
        elif self.agent_position == 15:
            reward += 10
            self.has_gpu = True
        elif self.agent_position == 0 and self.has_gpu:
            term = True
            reward += 10
        return self.agent_position, reward, term, False, None
