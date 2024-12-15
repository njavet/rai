import numpy as np

# project imports
from frozenlake.policy.random_mc import MonteCarloRandom
from frozenlake.helpers import argmax


class MonteCarloInc(MonteCarloRandom):
    def __init__(self, env, params):
        super().__init__(env, params)

    def choose_action(self, state):
        """ with probability epsilon:
                select an action randomly
            else
                select the action with the highest q-value """
        if np.random.rand() < self.params.epsilcon:
            action = self.env.action_space.sample()
        else:
            action = argmax(self.qtable[state])
        return action
