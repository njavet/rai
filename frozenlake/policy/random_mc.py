from collections import defaultdict
import numpy as np
from gymnasium.wrappers.common import TimeLimit

# project imports
from frozenlake.policy.base import BasePolicy


class MonteCarloRandom(BasePolicy):
    def __init__(self, action_space, obs_space_size, action_space_size):
        super().__init__(action_space, obs_space_size, action_space_size)

    def choose_action(self, state):
        action = self.action_space.sample()
        return action

    def update_qtable(self, state, reward, action):
        self.qtable[state, action] = reward
