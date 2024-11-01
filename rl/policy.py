from collections import defaultdict
import numpy as np
from gymnasium.wrappers.common import TimeLimit

# project imports
from rl.config import Params
from rl.eps_greedy import EpsilonGreedy


class MonteCarloRandomPolicy:
    def __init__(self, env, params: Params, debug: bool = False):
        self.env = env
        self.params = params
        self.debug = debug
        self.rewards = np.zeros((params.total_episodes, params.n_runs))
        self.steps = np.zeros((params.total_episodes, params.n_runs))
        self.episodes = np.arange(params.total_episodes)
        self.qtables = np.zeros((params.n_runs, env.observation_space.n, env.action_space.n))

    def choose_action(self):
        action = self.env.action_space.sample()
        return action

    def run(self):
        returns_sum = defaultdict(float)
        returns_count = defaultdict(float)
        value_function = np.zeros(self.env.observation_space.n)
        for episode in range(self.params.total_episodes):
            buffer = []
            state = self.env.reset()
            done = False
            while not done:
                action = self.choose_action()
                new_state, reward, done, _, _ = self.env.step(action)
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


# TODO refactor
class MonteCarloIncPolicy(MonteCarloRandomPolicy):
    def __init__(self, env, params: Params, debug: bool = False):
        super().__init__(env, params, debug)
        self.explorer = EpsilonGreedy(self.params.epsilon)
        self.q_table = np.zeros((self.env.observation_space.n, self.env.action_space.n))

    def run(self):
        state_counts = defaultdict(int)
        for episode in range(self.params.total_episodes):
            state, info = self.env.reset()
            buffer = []

            done = False
            while not done:
                action = self.explorer.choose_action(self.env.action_space, state, self.q_table)
                new_state, reward, done, _, _ = self.env.step(action)
                buffer.append((state, action, reward))
                state = new_state

            episode_reward = 0
            for t in reversed(range(len(buffer))):
                state, action, reward = buffer[t]
                episode_reward = self.params.gamma * episode_reward + reward

                if not any((state == x[0] and action == x[1]) for x in buffer[:t]):
                    state_counts[(state, action)] += 1
                    alpha = 1 / state_counts[(state, action)]
                    self.q_table[state, action] += alpha * (episode_reward - self.q_table[state, action])

