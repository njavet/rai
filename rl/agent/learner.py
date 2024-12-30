from abc import ABC
import numpy as np


class Learner(ABC):
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.value = np.zeros(params.state_size)
        self.qtable = np.zeros((params.state_size, params.action_size))


