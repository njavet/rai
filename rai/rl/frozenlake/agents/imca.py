import numpy as np

# project imports
from rai.rl.frozenlake.agents.base import Agent


class IMCAgent(Agent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.returns = np.zeros((params.state_size, params.action_size))
        self.counts = np.zeros((params.state_size, params.action_size))

    def get_action(self, state):
        if np.random.rand() < self.params.epsilon:
            action = self.env.action_space.sample()
        else:
            action = self.get_optimal_action(state)
        return action

    def run_episode(self):
        trajectory = self.generate_trajectory(self.get_action)
        episode_reward = 0
        for i, t in enumerate(reversed(trajectory)):
            state, action, reward = t.state, t.action, t.reward
            episode_reward += reward
            self.returns[state, action] += episode_reward
            self.counts[state, action] += 1
        self.update()

    def update(self):
        self.qtable = np.divide(self.returns,
                                self.counts,
                                out=np.zeros_like(self.returns),
                                where=self.counts != 0)
        self.vtable = np.max(self.qtable, axis=1)
