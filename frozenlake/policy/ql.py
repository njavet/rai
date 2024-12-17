from collections import defaultdict
import numpy as np

# project imports
from frozenlake.helpers import rand_argmax
from frozenlake.policy.inc_mc import MonteCarloInc


class Qlearning(MonteCarloInc):
    def __init__(self, env, params):
        super().__init__(env, params)

    def update_qtable(self, state, action, reward, new_state):
        """ Q-function update
            Q_update(s,a):= Q(s,a) + learning_rate * delta
                delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """

        # Compute the temporal difference (TD) target
        bfq = self.params.gamma * rand_argmax(self.qtable[new_state])
        delta = reward + bfq - self.qtable[state, action]

        self.qtable[state, action] = (
            self.qtable[state, action] + self.params.alpha * delta
        )
