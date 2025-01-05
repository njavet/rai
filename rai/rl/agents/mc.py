import numpy as np
import gymnasium as gym
from collections import defaultdict

# project imports
from rai.rl.agents.learner import Learner
from rai.utils.helpers import random_argmax


class MonteCarlo(Learner):
    def __init__(self,
                 env: gym.Env,
                 n_runs: int,
                 n_episodes: int,
                 gamma: float,
                 epsilon: float,
                 epsilon_min: float,
                 decay: float,
                 fv: bool) -> None:
        super().__init__(env, n_runs, n_episodes)
        self.gamma = gamma
        self.eps = epsilon
        self.eps_min = epsilon_min
        self.decay = decay
        self.fv = fv
        self.qtable = np.zeros((env.observation_space.n,
                                env.action_space.n))
        self.returns = defaultdict(list)
        self.counts = defaultdict(int)
        self.trajectories = defaultdict(list)

    def policy(self, state):
        if np.random.rand() < self.eps:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_episode(self, episode):
        if self.fv:
            self._process_fv()
        else:
            self._process_ev()
        self.eps = max(self.eps_min, self.decay * self.eps)

    def _process_fv(self):
        total_reward = 0
        visited_states = set()
        for ts in reversed(self.trajectory.steps):
            s, a, r = ts.state, ts.action, ts.reward
            total_reward = self.gamma * total_reward + r
            if s not in visited_states:
                visited_states.add(s)
                self.returns[(s, a)].append(total_reward)
                self.qtable[s, a] = np.mean(self.returns[(s, a)])

    def _process_ev(self):
        total_reward = 0
        for ts in reversed(self.trajectory.steps):
            s, a, r = ts.state, ts.action, ts.reward
            total_reward = self.gamma * total_reward + r
            self.counts[(s, a)] += 1
            self.returns[(s, a)].append(total_reward)

        for (s, a), rewards in self.returns.items():
            if rewards:
                self.qtable[s, a] = np.mean(rewards) / self.counts[(s, a)]

    def learn(self):
        qtables = np.zeros((self.n_runs,
                            self.env.observation_space.n,
                            self.env.action_space.n))
        for n in range(self.n_runs):
            self.returns = defaultdict(list)
            self.counts = defaultdict(int)
            self.qtable = np.zeros((self.env.observation_space.n,
                                    self.env.action_space.n))
            self.eps = 1.
            for episode in range(self.n_episodes):
                self.generate_trajectory()
                # collect all trajectories
                self.trajectories[(n, episode)] = self.trajectory
                self.process_episode(episode)
                qtables[n, :, :] = self.qtable
            qtable = np.mean(qtables, axis=0)
            vtable = np.sum(qtable, axis=1)
            print(f'run {n} done...')
        self.qtable = np.mean(qtables, axis=0)
