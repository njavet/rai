from abc import ABC
import numpy as np
from collections import defaultdict


class BasePolicy(ABC):
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.qtables = None
        self.qtable = None
        self.trajectories = defaultdict(list)

    def choose_action(self, state):
        raise NotImplementedError

    def reset_qtables(self):
        self.qtables = np.zeros((self.params.n_runs,
                                 self.env.observation_space.n,
                                 self.env.action_space.n))
        self.qtable = np.zeros((self.env.observation_space.n,
                                self.env.action_space.n))

    def update_qtable(self, *args):
        raise NotImplementedError

    def run(self):
        self.reset_qtable()
        rewards = np.zeros((self.params.total_episodes, self.params.n_runs))
        steps = np.zeros((self.params.total_episodes, self.params.n_runs))
        episodes = np.arange(self.params.total_episodes)
        all_states = []
        all_actions = []

        for i in range(self.params.n_runs):
            for episode in range(self.params.total_episodes):
                done = False
                state, info = self.env.reset()
                total_steps = 0
                total_rewards = 0
                while not done:
                    action = self.choose_action(state)
                    next_state, reward, term, trunc, info = self.env.step(action)

                    # update and collect
                    all_actions.append(action)
                    all_states.append(state)
                    total_rewards += reward
                    total_steps += 1
                    self.trajectories[i].append((state, reward, action))
                    self.update_qtable( state, reward, action)

                    done = term or trunc
                self.update_qtable( next_state, total_rewards, action)
            rewards[episode, i] = total_rewards
            steps[episode, i] = steps
            self.qtables[i, :, :] = self.qtable
        return self.qtables.mean(axis=0), total_steps, rewards, episodes, all_actions, all_states
