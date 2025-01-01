import numpy as np

# project imports
from rai.rl.agents.learner import Learner
from rai.utils.helpers import random_argmax


class Q2Learner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.alpha = params.alpha
        self.gamma = params.gamma
        self.eps = params.epsilon
        self.eps_min = params.epsilon_min
        self.decay = params.decay
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.q0 = np.zeros((params.state_size, params.action_size))
        self.q1 = np.zeros((params.state_size, params.action_size))

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
        gamma = self.params.gamma
        alpha = self.params.alpha

        if np.random.random() <= 0.5:
            a_max = random_argmax(self.q0[ns, a])
            tmp = alpha * (r + gamma * self.q1[ns, a_max] - self.q0[s, a])
            self.q0[s, a] = self.q0[s, a] + tmp
        else:
            a_max = random_argmax(self.q1[ns, a])
            tmp = alpha * (r + gamma * self.q0[ns, a_max] - self.q1[s, a])
            self.q1[s, a] = self.q1[s, a] + tmp
        self.qtable = (self.q0 + self.q1) / 2

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
