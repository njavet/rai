import numpy as np

# project imports
from frozenlake.policy.random_mc import MonteCarloRandom
from frozenlake.helpers import rand_argmax


class MonteCarloInc(MonteCarloRandom):
    def __init__(self, env, params):
        super().__init__(env, params)

    def choose_action(self, state):
        if np.random.rand() < self.params.epsilcon:
            action = self.env.action_space.sample()
        else:
            action = rand_argmax(self.qtable[state])
        return action
