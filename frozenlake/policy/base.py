from abc import ABC
import numpy as np
from collections import defaultdict


class BasePolicy(ABC):
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.qtable = None
        self.qtables = None
        self.trajectories = defaultdict(list)

    def choose_action(self, state):
        raise NotImplementedError

    def reset_qtable(self):
        self.qtables = np.zeros((self.params.n_runs,
                                 self.env.observation_space.n,
                                 self.env.action_space.n))

    def update_qtable(self, *args):
        raise NotImplementedError

    def run(self):
        self.reset_qtable()
        self.qtable = np.zeros((self.env.observation_space.n,
                                self.env.action_space.n))
        rewards = np.zeros((self.params.total_episodes, self.params.n_runs))
        total_steps = np.zeros((self.params.total_episodes, self.params.n_runs))
        episodes = np.arange(self.params.total_episodes)
        all_states = []
        all_actions = []

        for i in range(self.params.n_runs):
            for episode in range(self.params.total_episodes):
                done = False
                state, info = self.env.reset()
                steps = 0
                total_rewards = 0
                while not done:
                    action = self.choose_action(state)
                    all_actions.append(action)
                    all_states.append(state)
                    next_state, reward, term, trunc, info = self.env.step(action)
                    total_rewards += reward
                    steps += 1
                    self.trajectories[i].append((state, reward, action))
                    self.update_qtable( state, reward, action)
                    if trunc:
                        print(steps)
                    done = term or trunc
                self.update_qtable( next_state, total_rewards, action)
            rewards[episode, i] = total_rewards
            total_steps[episode, i] = steps
            self.qtables[i, :, :] = self.qtable
        return self.qtables.mean(axis=0), total_steps, rewards, episodes, all_actions, all_states
