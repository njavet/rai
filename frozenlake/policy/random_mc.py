# project imports
from frozenlake.policy.base import BasePolicy


class MonteCarloRandom(BasePolicy):
    def __init__(self, env, params):
        super().__init__(env, params)

    def choose_action(self, state):
        action = self.env.action_space.sample()
        return action

    def update_qtable(self, state, reward, action):
        self.qtable[state, action] = reward
