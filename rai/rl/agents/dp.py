import numpy as np
import gymnasium as gym
from collections import defaultdict

# project imports
from rai.rl.agents.learner import Learner


class DP(Learner):
    """ dynamic programming learner for frozenlake"""

    def __init__(self, env: gym.Env, n_runs: int, n_episodes: int, model=None):
        super().__init__(env, n_runs, n_episodes)
        self.model = model
        self.size = None
        self.holes = None
        self.is_slippery = env.spec.kwargs['is_slippery']
        self.values = np.zeros(self.env.observation_space.n)
        self.qtable = np.zeros((self.env.observation_space.n,
                                self.env.action_space.n))
        self.pi = defaultdict(int)
        self.get_info()

    def reset(self):
        super().reset()
        self.values = np.zeros(self.env.observation_space.n)
        self.qtable = np.zeros((self.env.observation_space.n,
                                self.env.action_space.n))

    def policy(self, state: int) -> int:
        return self.pi[state]

    def compute_optimal_value_function(self, n_iter: int) -> None:
        # V(s) = 0
        self.reset()
        for i in range(n_iter):
            for state in range(self.env.observation_space.n):
                lst0 = []
                for action in range(self.env.action_space.n):
                    val = self._compute_state_action_value(state, action)
                    lst0.append((action, val))
                lst1 = sorted(lst0, key=lambda x: x[1], reverse=True)
                a, v = lst1[0]
                self.values[state] = v
                self.pi[state] = a

    def get_position(self, state: int) -> tuple[int, int]:
        m, n = divmod(state, self.size)
        return m, n
    def get_info(self):
        arr = self.env.unwrapped.desc.astype(str)
        self.size = arr.shape[0]
        self.holes = np.argwhere(arr == 'H').tolist()

    def get_perpendicular_actions(self, action: int):
        if action == 0 or action == 2:
            return 1, 3
        elif action == 1 or action == 3:
            return 0, 2

    def _compute_state_action_value(self, state: int, action: int) -> float:
        # TODO params transistion probas
        p0, p1 = self.model.get_per

        pass

