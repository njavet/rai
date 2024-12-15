from collections import defaultdict
import numpy as np

# project imports
from frozenlake.policy.inc_mc import MonteCarloInc


class Qlearning(MonteCarloInc):
    def __init__(self, action_space, obs_space_size, action_space_size, eps):
        super().__init__(action_space, obs_space_size, action_space_size, eps)

    def update_qtable(self, state, action, reward, term, new_state):
        """ Q-function update
            Q_update(s,a):= Q(s,a) + learning_rate * delta
                delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """

        # Compute the temporal difference (TD) target
        bfq = (not term) * argmax(self.qtable[new_state])
        delta = reward + self.params.gamma * bfq - self.qtable[state, action]

        self.qtable[state, action] = (
            self.qtable[state, action] + self.params.learning_rate * delta
        )
