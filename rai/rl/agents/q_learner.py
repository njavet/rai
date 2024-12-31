import numpy as np

# project imports
from rai.rl.agents.base import Learner
from rai.utils.helpers import random_argmax


class QLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)

    def policy(self, state):
        if np.random.rand() < self.params.epsilon:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_step(self, next_state):
        """ Q-function update
             Q_update(s,a):= Q(s,a) + learning_rate * delta
                 delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """
        # Compute the temporal difference (TD) target
        ts = self.trajectory.steps[-1]
        state, action, reward = ts.state, ts.action, ts.reward
        bfq = self.params.gamma * np.argmax(self.qtable[next_state])
        delta = self.params.alpha * (reward + bfq - self.qtable[state, action])
        self.qtable[state, action] = self.qtable[state, action] + delta
