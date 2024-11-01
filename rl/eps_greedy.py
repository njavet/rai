import numpy as np

# project imports
from rl.helpers import argmax


class EpsilonGreedy:
    def __init__(self, epsilon):
        self.epsilon = epsilon

    def choose_action(self, action_space, state, qtable):
        """ with probability epsilon:
                select an action randomly
            else
                select the action with the highest q-value """
        if np.random.rand() < self.epsilon:
            action = action_space.sample()
        else:
            action = argmax(qtable[state])
        return action
