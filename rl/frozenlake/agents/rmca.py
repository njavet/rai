import numpy as np

# project imports
from rl.frozenlake.agents.base import Agent


class RMCAgent(Agent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.returns = np.zeros((params.state_size, params.action_size))
        self.counts = np.zeros((params.state_size, params.action_size))

    def get_action(self, state):
        action = self.env.action_space.sample()
        return action

    def update(self):
        self.qtable = np.divide(self.returns,
                                self.counts,
                                out=np.zeros_like(self.returns),
                                where=self.counts != 0)
        self.vtable = np.max(self.qtable, axis=1)
