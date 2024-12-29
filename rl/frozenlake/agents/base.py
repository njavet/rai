from abc import ABC
import gymnasium as gym


class Agent(ABC):
    def __init__(self, env: gym.Env):
        self.env = env

    def get_action(self, state):
        raise NotImplementedError

    def policy(self, state):
        raise NotImplementedError
