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
        """TODO: Change the following code to implement the update of the Q-function
            Q_update(s,a):= Q(s,a) + learning_rate * delta
                delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)]"""

        q_update = self.qtable[state, action]
        return q_update

    def reset_qtable(self):
        """Reset the Q-table."""
        self.qtable = np.zeros((self.state_size, self.action_size))
