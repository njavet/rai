import numpy as np


class Qlearning:
    def __init__(self, learning_rate, gamma, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.reset_qtable()
        self.qtable = np.zeros((self.state_size, self.action_size))

    def update(self, state, action, reward, new_state):
        """ Q-function update
            Q_update(s,a):= Q(s,a) + learning_rate * delta
                delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """

        # Compute the temporal difference (TD) target
        best_future_q = np.max(self.qtable[new_state])  # max Q(s', a')
        delta = reward + self.gamma * best_future_q - self.qtable[state, action]

        # Update the Q-value
        q_update = self.qtable[state, action] + self.learning_rate * delta
        return q_update

    def reset_qtable(self):
        """Reset the Q-table."""
        self.qtable = np.zeros((self.state_size, self.action_size))


def get_q_learner(params, action_size, state_size):
    learner = Qlearning(learning_rate=params.learning_rate,
                        gamma=params.gamma,
                        state_size=state_size,
                        action_size=action_size, )

    return learner
