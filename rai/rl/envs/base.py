"""
should provide the same interface as the gym env,
a step and reset function with discrete action and state spaces
"""
from abc import ABC
import numpy as np


class BaseEnv(ABC):
    def __init__(self, name: str):
        self.name = name
        # TODO generalize
        self.obs_space = ObservationSpace(size=16, start=0, terminal=15)
        self.action_space = ActionSpace(size=4)
        self.goal_pos = 15
        self.agent_pos = 0

    def reset(self):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError


class ObservationSpace:
    def __init__(self, size, start, terminal):
        self.size = size
        self.start = start
        self.terminal = terminal


class ActionSpace:
    def __init__(self, size):
        self.size = size
        pass

    def sample(self):
        return np.random.randint(0, self.size)
