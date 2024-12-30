import numpy as np
from collections import defaultdict

# project imports
from rai.agents.base import SchopenhauerAgent
from rai.utils.helpers import random_argmax


class RLAgent(SchopenhauerAgent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.vtable = np.zeros(params.state_size)
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.trajectories = defaultdict(list)

    def get_optimal_action(self, state: int) -> int:
        action = random_argmax(self.qtable[state])
        return action


class Learner(RLAgent):
    def __init__(self, env, params):
        super().__init__(env, params)

    def get_action(self, state: int) -> int:
        raise NotImplementedError
