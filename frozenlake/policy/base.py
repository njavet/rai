from abc import ABC
import numpy as np
from collections import defaultdict


class BasePolicy(ABC):
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.qtables = None
        self.trajectories = defaultdict(list)

    def choose_action(self, state):
        raise NotImplementedError

    def reset_qtable(self):
        self.qtables = np.zeros((params.n_runs,
                                 env.observation_space.n,
                                 env.action_space.n))

    def update_qtable(self, *args):
        raise NotImplementedError

    def run(self, params, env):
        self.reset_qtable()
        for i in range(params.n_runs):
            for episode in range(params.total_episodes):
                done = False
                state, info = env.reset()
                total_rewards = 0
                while not done:
                    action = self.choose_action(state)
                    next_state, reward, term, trunc, info = env.step(action)
                    total_rewards += reward
                    self.trajectories[i].append((state, reward, action))
                    self.update_qtable(i, state, reward)
                    done = term or trunc
                self.update_qtable(i, next_state, total_rewards)
        return self.qtables.mean(axis=0)
