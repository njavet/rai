import numpy as np
from collections import defaultdict

# project imports
from rai.rl.agents.learner import Learner
from rai.utils.helpers import random_argmax


class DP:
    """ dynamic programming learner """
    def __init__(self):
        # self.qtable = np.zeros((params.state_size, action_space.n))
        self.vtable = np.zeros(16)
        self.policy = defaultdict(int)

    @staticmethod
    def reward_table(state, next_state):
        if (state, next_state) in [(0, 1),
                                     (1, 2),
                                     (2, 3),
                                     (3, 7),
                                     (7, 6),
                                     (6, 5),
                                     (5, 4),
                                     (4, 8),
                                     (8, 9),
                                     (9, 10),
                                     (10, 11),
                                     (11, 15)]:
            return 1
        else:
            return 0

    def pos_to_tuple(self, state):
        """ convert integer position to grid position"""
        x, y = divmod(state, 4)
        return x, y

    @staticmethod
    def get_action_values(action):
        if action == 0:
            return 0, -1
        elif action == 1:
            return 1, 0
        elif action == 2:
            return 0, 1
        elif action == 3:
            return -1, 0
        raise ValueError('invalid action')

    def get_next_state(self, state, action):
        x, y = self.pos_to_tuple(state)
        ax, ay = self.get_action_values(action)
        x1 = max(x + ax, 0)
        y1 = max(y + ay, 0)
        x_new = min(x1, 3)
        y_new = min(y1, 3)
        return x_new * 4 + y_new

    def compute_optimal_value_function(self, h):
        # v0
        self.vtable = np.zeros(16)
        for i in range(h):
            # vk = max(R(state, action, nextstate) + gamma * vk-1(nextstate)
            for state in range(16):
                lst = []
                for action in range(4):
                    ns = self.get_next_state(state, action)
                    r = self.reward_table(state, ns)
                    curr = r + self.vtable[ns]
                    lst.append((action, r, curr))
                lst = sorted(lst, key=lambda x: x[1], reverse=True)
                a, r, v = lst[0]
                print('state', state, 'action', a, 'v', v)
                self.vtable[state] = v
                self.policy[state] = a
        return self.vtable.reshape((4, 4))
