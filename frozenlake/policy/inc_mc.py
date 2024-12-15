import numpy as np

# project imports
from frozenlake.policy.base import BasePolicy
from frozenlake.helpers import argmax


class MonteCarloInc(BasePolicy):
    def __init__(self, action_space, obs_space_size, action_space_size, eps):
        super().__init__()
        self.eps = eps

    def choose_action(self, state):
        """ with probability epsilon:
                select an action randomly
            else
                select the action with the highest q-value """
        if np.random.rand() < self.eps:
            action = self.action_space.sample()
        else:
            action = argmax(self.qtable[state])
        return action
