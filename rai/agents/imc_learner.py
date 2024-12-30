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
