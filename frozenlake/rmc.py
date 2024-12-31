from rich.console import Console
from collections import defaultdict
import numpy as np

# project imports
from frozenlake.utils.helpers import rand_argmax


class Agent:
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.counts = defaultdict(int)
        self.values = defaultdict(float)
        self.qtable = np.zeros((env.observation_space.n, env.action_space.n))
        self.trajectories = None
        self.console = Console()

    def run(self):
        self.trajectories = {}
        for episode in range(self.params.total_episodes):
            self.run_episode(episode)
            self.learn(episode)

    def state_action_value(self, state, action):
        key = state, action
        try:
            value = self.values[key] / self.counts[key]
        except ZeroDivisionError:
            value = 0
        return value

    def learn(self, i):
        total_reward = 0
        for state, reward, action in self.trajectories[i][::-1]:
            key = state, action
            total_reward += reward
            self.counts[key] += 1
            self.values[key] += total_reward

        for state, action in self.values.keys():
            self.qtable[state, action] = self.state_action_value(state, action)

    def run_episode(self, i):
        state, info = self.env.reset()
        trajectory = []
        while True:
            action = self.env.action_space.sample()
            next_state, reward, term, trunc, info = self.env.step(action)
            trajectory.append((state, reward, action))
            state = next_state
            if trunc or term:
                break
        self.trajectories[i] = trajectory

    def pprint_q_table(self):
        for i in range(4):
            self.console.print(16*'-', style='cyan')
            values = []
            for j in range(4):
                val = rand_argmax(self.qtable[i + j])
                values.append(f'{val:.2f}')
            self.console.print(' | '.join(values))
        self.console.print(16*'-', style='cyan')

        print(self.values, self.counts)