import numpy as np
import gymnasium as gym
from collections import defaultdict

# project imports
from rai.rl.agents.schopenhauer import SchopenhauerAgent
from rai.utils.helpers import random_argmax


class QAgent(SchopenhauerAgent):
    def __init__(self,
                 env: gym.Env,
                 alpha: float,
                 gamma: float,
                 epsilon: float,
                 epsilon_min: float,
                 decay: float,
                 double_q: bool = False) -> None:
        super().__init__(env)
        self.alpha = alpha
        self.gamma = gamma
        self.eps = epsilon
        self.eps_min = epsilon_min
        self.decay = decay
        self.double_q = double_q
        self.qtable = np.zeros((env.observation_space.n, env.action_space.n))
        self.q0 = np.zeros((env.observation_space.n, env.action_space.n))
        self.q1 = np.zeros((env.observation_space.n, env.action_space.n))
        self.trajectories = defaultdict(list)

    def policy(self, state: int) -> int:
        if np.random.rand() < self.eps:
            action = self.env.action_space.sample()
        elif np.random.rand() < 0.5:
            action = random_argmax(self.q0[state])
        else:
            action = random_argmax(self.q1[state])
        return action

    def process_step(self) -> None:
        # q learning
        ts = self.trajectory.steps[-1]
        s, a, r, ns = ts.state, ts.action, ts.reward, ts.next_state

        if ts.terminal:
            tmp = r - self.q0[s, a]
            self.q0[s, a] += self.alpha * tmp
        elif np.random.rand() < 0.5:
            q0_action = random_argmax(self.q0[ns])
            tmp = r + self.gamma * self.q1[ns, q0_action] - self.q0[s, a]
            self.q0[s, a] += self.alpha * tmp
        else:
            q1_action = random_argmax(self.q1[ns])
            tmp = r + self.gamma * self.q0[ns, q1_action] - self.q1[s, a]
            self.q1[s, a] += self.alpha * tmp

    def process_episode(self, episode: int) -> None:
        self.eps = max(self.eps_min, self.decay * self.eps)

    def learn(self, n_runs, n_episodes):
        qtables = np.zeros((n_runs,
                            self.env.observation_space.n,
                            self.env.action_space.n))
        for run in range(n_runs):
            self.q0 = np.zeros((self.env.observation_space.n,
                                self.env.action_space.n))
            self.q1 = np.zeros((self.env.observation_space.n,
                                self.env.action_space.n))
            if not self.double_q:
                self.q0 = self.q1
            self.eps = 1.
            for episode in range(n_episodes):
                self.generate_trajectory()
                self.trajectories[(run, episode)] = self.trajectory
                self.process_episode(episode)
                qtables[run, :, :] = np.mean(self.q0 + self.q1)
            print(f'run {run} done...')
        self.qtable = np.mean(qtables, axis=0)
