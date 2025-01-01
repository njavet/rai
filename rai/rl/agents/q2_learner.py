import numpy as np

# project imports
from rai.rl.agents.learner import Learner
from rai.utils.helpers import random_argmax


class QLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.q0 = np.zeros((params.state_size, params.action_size))
        self.q1 = np.zeros((params.state_size, params.action_size))

    def policy(self, state):
        epsilon = max(self.params.epsilon_min, self.params.epsilon * self.params.decay)
        if np.random.rand() < epsilon:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_step(self, next_state):
        """ Q-function update
             Q_update(s,a):= Q(s,a) + learning_rate * delta
                 delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """
        ts = self.trajectory.steps[-1]
        s, a, r = ts.state, ts.action, ts.reward
        gamma = self.params.gamma
        alpha = self.params.alpha

        if np.random.random() <= 0.5:
            a_max = random_argmax(self.q0[next_state, a])
            tmp = alpha * (r + gamma * self.q1[next_state, a_max] - self.q0[s, a])
            self.q0[s, a] = self.q0[s, a] + tmp
        else:
            a_max = random_argmax(self.q1[next_state, a])
            tmp = alpha * (r + gamma * self.q0[next_state, a_max] - self.q1[s, a])
            self.q1[s, a] = self.q1[s, a] + tmp
