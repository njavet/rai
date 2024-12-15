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
        self.qtable = np.zeros((self.env.observation_space.n, self.env.action_space.n))
        self.qtables = np.zeros((params.n_runs, env.observation_space.n, env.action_space.n))

    def choose_action(self, state):
        action = self.env.action_space.sample()
        return action

    def reset_qtable(self):
        self.qtable = np.zeros((self.env.observation_space.n, self.env.action_space.n))

    def run(self):
        all_actions = []
        all_states = []
        for i in range(self.params.n_runs):
            self.reset_qtable()

            for episode in range(self.params.total_episodes):
                buffer = []
                state, info = self.env.reset()
                step = 0
                total_rewards = 0
                done = False
                while not done:
                    action = self.choose_action(state)
                    all_states.append(state)
                    all_actions.append(action)
                    new_state, reward, done, _, _ = self.env.step(action)
                    buffer.append((state, action, reward))
                    total_rewards += reward
                    step += 1
                    state = new_state
                self.rewards[episode, i] = total_rewards
                self.steps[episode, i] = step
            self.qtables[i, :, :] = self.qtable
        return self.rewards, self.steps, self.episodes, self.qtables, all_states, all_actions


# TODO refactor
class MonteCarloIncPolicy(MonteCarloRandomPolicy):
    def __init__(self, env, params: Params, debug: bool = False):
        super().__init__(env, params, debug)
        self.explorer = EpsilonGreedy(self.params.epsilon)

    def choose_action(self, state):
        action = self.explorer.choose_action(self.env.action_space, state, self.qtable)
        return action
