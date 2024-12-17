from abc import ABC
import numpy as np


class BasePolicy(ABC):
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.qtable = None

    def init_qtable(self, state_space_n, action_space_n):
        self.qtable = np.zeros((state_space_n, action_space_n))

    def choose_action(self, state):
        raise NotImplementedError

    def update_qtable(self, *args):
        raise NotImplementedError
