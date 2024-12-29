import numpy as np

# project imports
from rl.frozenlake.agents.base import Agent


class QAgent(Agent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.qtable = np.zeros((params.state_size, params.action_size))

    def get_action(self, state):
        if np.random.random() < self.params.epsilon:
            action = self.env.action_space.sample()
        else:
            action = np.argmax(self.qtable[state])
        return action

    def update(self, state, action, reward, next_state):
        pass


