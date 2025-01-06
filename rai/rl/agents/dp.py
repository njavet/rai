import numpy as np
import gymnasium as gym
from collections import defaultdict

# project imports
from rai.rl.agents.schopenhauer import SchopenhauerAgent


class DP(SchopenhauerAgent):
    """ dynamic programming learner for frozenlake"""

    def __init__(self,
                 env: gym.Env,
                 n_runs: int,
                 n_episodes: int,
                 gamma: float,
                 model=None):
        super().__init__(env, n_runs, n_episodes)
        self.gamma = gamma
        self.model = model
        self.size = None
        self.holes = None
        self.is_slippery = env.spec.kwargs['is_slippery']
        self.values = np.zeros(self.env.observation_space.n)
        self.qtable = np.zeros((self.env.observation_space.n,
                                self.env.action_space.n))
        self.pi = defaultdict(int)
        self.get_info()

    def reward_func(self, state, next_state):
        st = self.size * self.size - 1
        if state == st - 1 or state == st - self.size:
            if next_state == st:
                return 1
        return 0

    def get_info(self):
        arr = self.env.unwrapped.desc.astype(str)
        self.size = arr.shape[0]
        hs = np.argwhere(arr == 'H').tolist()
        self.holes = [t[0] * self.size + t[1] for t in hs]

    def get_next_state(self, state, action):
        m, n = divmod(state, self.size)
        if action == 0:
            am, an = 0, -1
        elif action == 1:
            am, an = 1, 0
        elif action == 2:
            am, an = 0, 1
        elif action == 3:
            am, an = -1, 0

        m1 = max(m + am, 0)
        n1 = max(n + an, 0)
        m_new = min(m1, self.size - 1)
        n_new = min(n1, self.size - 1)
        return m_new * self.size + n_new

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
                if state in self.holes or state == self.size * self.size - 1:
                    self.values[state] = 0
                    continue
                lst0 = []
                for action in range(self.env.action_space.n):
                    val = self._compute_state_action_value(state, action)
                    lst0.append((action, val))
                lst1 = sorted(lst0, key=lambda x: x[1], reverse=True)
                a, v = lst1[0]
                self.values[state] = v
                self.pi[state] = a

    def _compute_state_action_value(self, state: int, action: int) -> float:
        tprob = 1 / 3
        if action == 0 or action == 2:
            actions = [1, action, 3]
        else:
            actions = [0, action, 2]

        res = 0
        for a in actions:
            ns = self.get_next_state(state, a)
            rs = self.reward_func(state, ns)
            res += tprob * (rs + self.gamma * self.values[ns])
        return res
