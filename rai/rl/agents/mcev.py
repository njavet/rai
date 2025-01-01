import numpy as np
from collections import defaultdict

# project imports
from rai.rl.agents.learner import Learner
from rai.utils.helpers import random_argmax


class MonteCarloEV(Learner):
    """ first visit monte carlo learner """
    def __init__(self, env, params):
        super().__init__(env, params)
        self.gamma = params.gamma
        self.eps = params.epsilon
        self.eps_min = params.epsilon_min
        self.decay = params.decay
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.returns = defaultdict(list)
        self.counts = defaultdict(int)
        self.trajectories = defaultdict(list)

    def policy(self, state):
        epsilon = max(self.eps_min, self.eps * self.decay)
        if np.random.rand() < epsilon:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_trajectory(self, episode):
        total_reward = 0
        for ts in reversed(self.trajectory):
            s, a, r = ts.state, ts.action, ts.reward
            total_reward = self.gamma * total_reward + r
            self.counts[(s, a)] += 1
            self.returns[(s, a)].append(total_reward)
            self.qtable[s, a] = np.mean(self.returns[(s, a)]) / self.counts[(s, a)]

    def learn(self):
        qtables = np.zeros((self.params.n_runs,
                            self.params.state_size,
                            self.params.action_size))
        for n in range(self.params.n_runs):
            self.returns = defaultdict(list)
            self.counts = defaultdict(int)
            self.qtable = np.zeros((self.params.state_size, self.params.action_size))
            for episode in range(self.params.total_episodes):
                self.generate_trajectory()
                # collect all trajectories
                self.trajectories[(n, episode)] = self.trajectory
                self.process_trajectory(episode)
                qtables[n, :, :] = self.qtable
        self.qtable = np.mean(qtables, axis=0)
