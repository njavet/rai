import numpy as np
from collections import defaultdict

# project imports
from rai.rl.agents.learner import Learner
from rai.utils.helpers import random_argmax


class DP(Learner):
    """ dynamic programming learner """
    def __init__(self, obs_space, action_space, params=None):
        super().__init__(obs_space, action_space, params)
        self.values = np.zeros(self.obs_space.n)
        self.qtable = np.zeros((self.obs_space.n, self.action_space.n))
        self.pi = defaultdict(int)

    def reset(self):
        super().reset()
        self.values = np.zeros(self.obs_space.n)
        self.qtable = np.zeros((self.obs_space.n, self.action_space.n))

    def policy(self, state: int) -> int:
        return self.pi[state]

    def compute_optimal_value_function(self, n_iter: int) -> None:
        # V(s) = 0
        self.reset()
        for i in range(n_iter):
            for state in range(self.obs_space.n):
                lst0 = []
                for action in range(self.action_space.n):
                    val = self._compute_state_action_value(state, action)
                    lst0.append((action, val))
                lst1 = sorted(lst0, key=lambda x: x[1], reverse=True)
                a, v = lst1[0]
                self.values[state] = v
                self.pi[state] = a

    def _compute_state_action_value(self, state: int, action: int) -> float:
        # TODO params
        pass

