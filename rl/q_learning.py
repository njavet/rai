import numpy as np

# project imports
from rl.eps_greedy import EpsilonGreedy


class Qlearning:
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.state_size = env.observation_space.n
        self.action_size = env.action_space.n
        self.reset_qtable()
        self.qtable = np.zeros((self.state_size, self.action_size))
        self.explorer = EpsilonGreedy(self.params.epsilon)

    def update(self, state, action, reward, new_state):
        """ Q-function update
            Q_update(s,a):= Q(s,a) + learning_rate * delta
                delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """

        # Compute the temporal difference (TD) target
        best_future_q = np.max(self.qtable[new_state])  # max Q(s', a')
        delta = reward + self.params.gamma * best_future_q - self.qtable[state, action]

        # Update the Q-value
        q_update = self.qtable[state, action] + self.params.learning_rate * delta
        return q_update

    def reset_qtable(self):
        """Reset the Q-table."""
        self.qtable = np.zeros((self.state_size, self.action_size))

    def q_learning_algorithm(self):
        for episode in range(self.params.total_episodes):
            state = self.env.reset()
            done = False

            while not done:
                action = self.explorer.choose_action(self.env.action_space, state, self.qtable)
                new_state, reward, done, _, _ = self.env.step(action)
                self.qtable[state, action] = self.update(state, action, reward, new_state)
                state = new_state
        value_function = np.max(self.qtable, axis=1)
        return value_function
