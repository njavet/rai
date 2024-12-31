import numpy as np

# project imports
from rai.rl.agents.learner import Learner
from rai.utils.helpers import random_argmax


class MCLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)

    def policy(self, state):
        epsilon = max(self.params.epsilon_min, self.params.epsilon * self.params.decay)
        if np.random.rand() < epsilon:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_episode(self, episode):
        returns, counts = super().process_episode(episode)
        qtable = np.divide(returns,
                           counts,
                           out=np.zeros_like(returns),
                           where=counts != 0)
        self.qtable = (self.qtable + qtable) / 2
