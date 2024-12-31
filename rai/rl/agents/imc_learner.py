import numpy as np

# project imports
from rai.rl.agents.base import Learner
from rai.utils.helpers import random_argmax


class IMCLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)

    def policy(self, state):
        if np.random.rand() < self.params.epsilon:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_episode(self, episode):
        returns, count = super().process_episode(episode)
        self.update_qtable(returns, count)

    def update_qtable(self, returns, counts):
        qtable = np.divide(returns,
                           counts,
                           out=np.zeros_like(returns),
                           where=counts != 0)
        self.qtable = (self.qtable + qtable) / 2
