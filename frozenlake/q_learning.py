from collections import defaultdict
import numpy as np

# project imports
from rl.eps_greedy import EpsilonGreedy
from rl.helpers import argmax


class Qlearning:
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.state_size = env.observation_space.n
        self.action_size = env.action_space.n
        self.rewards = np.zeros((params.total_episodes, params.n_runs))
        self.steps = np.zeros((params.total_episodes, params.n_runs))
        self.episodes = np.arange(params.total_episodes)
        self.qtables = np.zeros((params.n_runs, self.state_size, self.action_size))
        self.qtable = np.zeros((self.state_size, self.action_size))
        self.explorer = EpsilonGreedy(self.params.epsilon)

    def update(self, state, action, reward, term, new_state):
        """ Q-function update
            Q_update(s,a):= Q(s,a) + learning_rate * delta
                delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """

        # Compute the temporal difference (TD) target
        bfq = (not term) * argmax(self.qtable[new_state])
        delta = reward + self.params.gamma * bfq - self.qtable[state, action]

        self.qtable[state, action] = (
            self.qtable[state, action] + self.params.learning_rate * delta
        )

    def reset_qtable(self):
        """Reset the Q-table."""
        self.qtable = np.zeros((self.state_size, self.action_size))

    def q_learning_algorithm(self):
        all_states = []
        all_actions = []
        for i in range(self.params.n_runs):
            self.reset_qtable()

            for episode in range(self.params.total_episodes):
                state, info = self.env.reset()
                step = 0
                done = False
                total_rewards = 0

                while not done:
                    action = self.explorer.choose_action(self.env.action_space, state, self.qtable)
                    all_states.append(state)
                    all_actions.append(action)
                    new_state, reward, done, trunc, info = self.env.step(action)
                    self.update(state, action, reward, done, new_state)
                    total_rewards += reward
                    step += 1
                    state = new_state
                self.rewards[episode, i] = total_rewards
                self.steps[episode, i] = step
            self.qtables[i, :, :] = self.qtable
        return self.rewards, self.steps, self.episodes, self.qtables, all_states, all_actions
