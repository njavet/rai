import numpy as np

# project imports
from rl.frozenlake.agents.base import Agent


class RMCAgent(Agent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.returns = np.zeros((params.state_size, params.action_size))
        self.counts = np.zeros((params.state_size, params.action_size))
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.state_value = np.zeros(params.state_size)

    def get_action(self, state, learning):
        return self.env.action_space.sample()

    def run_episode(self, learning=True):
        trajectory = self.generate_trajectory(learning)
        episode_reward = 0
        for i, t in enumerate(reversed(trajectory)):
            state, action, reward = t.state, t.action, t.reward
            episode_reward += reward
            self.returns[state, action] += episode_reward
            self.counts[state, action] += 1

    def update(self):
        self.qtable = np.divide(self.returns,
                                self.counts,
                                out=np.zeros_like(self.returns),
                                where=self.counts != 0)
        self.state_value = np.max(self.qtable, axis=1)
