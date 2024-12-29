from abc import ABC
import gymnasium as gym

# project imports
from rl.models import Params


class Agent(ABC):
    def __init__(self, env: gym.Env, params: Params):
        self.env = env
        self.params = params

    def get_action(self, state):
        raise NotImplementedError

    def policy(self, state):
        raise NotImplementedError
