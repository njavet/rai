import numpy as np
from collections import defaultdict

# project imports
from rai.agents.base import Learner
from rai.utils.helpers import random_argmax
from rai.utils.models import Params, TrajectoryStep, Trajectory


class RMCLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)

    def get_action(self, state):
        action = self.env.action_space.sample()
        return action

    def process_episodes(self):
        returns = np.zeros((self.params.state_size, self.params.action_size))
        counts = np.zeros((self.params.state_size, self.params.action_size))
        for episode, trajectories in self.trajectories.items():
            returns, counts = self.evaluate_trajectories(trajectories)
        self.update_qtable(returns, counts)

    def update_qtable(self, returns, counts):
        self.qtable = np.divide(returns,
                                counts,
                                out=np.zeros_like(returns),
                                where=counts != 0)
