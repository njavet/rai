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
        self.qtable = np.zeros((self.state_size, self.action_size))
        self.explorer = EpsilonGreedy(self.params.epsilon)

    def update(self, state, action, reward, term, new_state):
        """ Q-function update
            Q_update(s,a):= Q(s,a) + learning_rate * delta
                delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """

        # Compute the temporal difference (TD) target
        bfq = (not term) * np.max(self.qtable[new_state])
        delta = reward + self.params.gamma * bfq - self.qtable[state, action]

        self.qtable[state, action] = (
            self.qtable[state, action] + self.params.learning_rate * delta
        )

    def reset_qtable(self):
        """Reset the Q-table."""
        self.qtable = np.zeros((self.state_size, self.action_size))

    def q_learning_algorithm(self):
        for episode in range(self.params.total_episodes):
            state, info = self.env.reset()
            done = False

            while not done:
                action = self.explorer.choose_action(self.env.action_space, state, self.qtable)
                new_state, reward, done, trunc, info = self.env.step(action)
                self.update(state, action, reward, done, new_state)
                state = new_state

        return self.qtable
