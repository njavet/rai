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
        self.obs_space = ObservationSpace(size=16, start=0)
        self.action_space = ActionSpace(size=4)

    def reset(self) -> tuple[int, str]:
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError


class ObservationSpace:
    def __init__(self, size, start, terminal=None):
        self.size = size
        self.start = start
        self.terminal = None


class ActionSpace:
    def __init__(self, size):
        self.size = size
        pass

    def sample(self):
        return np.random.randint(0, self.size)
