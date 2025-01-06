import numpy as np
import gymnasium as gym
from collections import defaultdict

# project imports
from rai.rl.agents.schopenhauer import SchopenhauerAgent
from rai.utils.helpers import random_argmax


class TDAgent(SchopenhauerAgent):
    def __init__(self,
                 env: gym.Env,
                 alpha: float,
                 gamma: float,
                 epsilon: float,
                 epsilon_min: float,
                 decay: float) -> None:
        super().__init__(env)
        self.alpha = alpha
        self.gamma = gamma
        self.eps = epsilon
        self.eps_min = epsilon_min
        self.decay = decay
        self.vtable = np.zeros(env.observation_space.n)
        self.qtable = np.zeros((env.observation_space.n,
                                env.action_space.n))
        self.trajectories = defaultdict(list)

    def policy(self, state: int) -> int:
        if np.random.rand() < self.eps:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_step(self) -> None:
        # q learning
        ts = self.trajectory.steps[-1]
        s, a, r, ns = ts.state, ts.action, ts.reward, ts.next_state
        if ts.terminal:
            tmp = r - self.qtable[s, a]
        else:
            tmp = r + self.gamma * np.max(self.qtable[ns]) - self.qtable[s, a]
        self.qtable[s, a] += self.alpha * tmp

    def process_episode(self, episode: int) -> None:
        self.eps = max(self.eps_min, self.decay * self.eps)

    def learn(self, n_runs, n_episodes):
        qtables = np.zeros((n_runs,
                            self.env.observation_space.n,
                            self.env.action_space.n))
        for run in range(n_runs):
            self.qtable = np.zeros((self.env.observation_space.n,
                                    self.env.action_space.n))
            self.eps = 1.
            for episode in range(n_episodes):
                self.generate_trajectory()
                self.trajectories[(run, episode)] = self.trajectory
                self.process_episode(episode)
                qtables[run, :, :] = self.qtable
            print(f'run {run} done...')
        self.qtable = np.mean(qtables, axis=0)
