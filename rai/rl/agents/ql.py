import numpy as np

# project imports
from rai.rl.agents.learner import Learner
from rai.utils.helpers import random_argmax


class QLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.alpha = params.alpha
        self.gamma = params.gamma
        self.eps = params.epsilon
        self.eps_min = params.epsilon_min
        self.decay = params.decay
        self.qtable = np.zeros((params.state_size, params.action_size))

    def policy(self, state):
        epsilon = max(self.eps_min, self.eps * self.decay)
        if np.random.rand() < epsilon:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_step(self):
        ts = self.trajectory.steps[-1]
        s, a, r, ns = ts.state, ts.action, ts.reward, ts.next_state
        bfq = self.gamma * np.max(self.qtable[ns])
        delta = self.alpha * (r + bfq - self.qtable[s, a])
        self.qtable[s, a] = self.qtable[s, a] + delta

    def learn(self):
        qtables = np.zeros((self.params.n_runs,
                            self.params.state_size,
                            self.params.action_size))
        for n in range(self.params.n_runs):
            self.qtable = np.zeros((self.params.state_size, self.params.action_size))
            for episode in range(self.params.total_episodes):
                self.generate_trajectory()
                # collect all trajectories
                self.trajectories[(n, episode)] = self.trajectory
                self.process_trajectory(episode)
                qtables[n, :, :] = self.qtable
        self.qtable = np.mean(qtables, axis=0)
