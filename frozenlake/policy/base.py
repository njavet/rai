from abc import ABC
import numpy as np


class BasePolicy(ABC):
    def __init__(self, action_space, obs_space_size, action_space_size):
        self.action_space = action_space
        self.qtable = np.zeros((obs_space_size, action_space_size))

    def choose_action(self, state):
        raise NotImplementedError

    def reset_qtable(self):
        self.qtable = np.zeros((obs_space_size, action_space_size))
