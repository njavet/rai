import numpy as np
from collections import defaultdict

# project imports
from rai.agents.base import Learner
from rai.utils.helpers import random_argmax
from rai.utils.models import Params, TrajectoryStep, Trajectory


class IMCLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)

    def get_action(self, state):
        if np.random.rand() < self.params.epsilon:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_episode(self, episode):
        returns = np.zeros((self.params.state_size, self.params.action_size))
        counts = np.zeros((self.params.state_size, self.params.action_size))
        for trajectory in self.trajectories[episode]:
            rs, cs = self.evaluate_trajectory(trajectory)
            returns += rs
            counts += cs
        self.update_qtable(returns, counts)

    def update_qtable(self, returns, counts):
        self.qtable = np.divide(returns,
                                counts,
                                out=np.zeros_like(returns),
                                where=counts != 0)
