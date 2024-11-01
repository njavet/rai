from collections import defaultdict
from typing import List
import numpy as np
import random
from gymnasium.wrappers.common import TimeLimit

# project imports
from rl.config import Params


class MonteCarloRandomPolicy:
    def __init__(self, env: TimeLimit, params: Params, debug: bool = False):
        self.env = env
        self.params = params
        self.debug = debug

    def run(self) -> np.ndarray:
        returns_sum = defaultdict(float)
        returns_count = defaultdict(float)
        value_function = np.zeros(self.env.observation_space.n)
        for episode in range(self.params.total_episodes):
            buffer = []
            state = self.env.reset()
            done = False
            while not done:
                action = self.env.action_space.sample()
                new_state, reward, done, _ = self.env.step(action)
                buffer.append((state, action, reward))
                state = new_state

            episode_reward = 0
            for t in reversed(range(len(buffer))):
                state, action, reward = buffer[t]
                episode_reward = self.params.gamma * episode_reward + reward

                if not any(state == x[0] for x in buffer[:t]):
                    returns_sum[state] += episode_reward
                    returns_count[state] += 1
                    value_function[state] = returns_sum[state] / returns_count[state]
        return value_function
