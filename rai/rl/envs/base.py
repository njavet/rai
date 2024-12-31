"""
should provide the same interface as the gym env,
a step and reset function with discrete action and state spaces
"""
from abc import ABC


class BaseEnv(ABC):
    def __init__(self, *args):
        self.state_size: int
        self.action_size: int

    def reset(self):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError
