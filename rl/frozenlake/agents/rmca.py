import numpy as np

# project imports
from rl.frozenlake.agents.base import Agent


class RMCAgent(Agent):
    def __init__(self, env, params):
        super().__init__(env, params)

    def get_action(self, state):
        action = self.env.action_space.sample()
        return action

    def evaluate_trajectories(self):
        returns = np.zeros((self.params.state_size, self.params.action_size))
        counts = np.zeros((self.params.state_size, self.params.action_size))
        for episode, trajectories in self.trajectories.items():
            for trajectory in trajectories:
                episode_reward = 0
                for t in reversed(trajectory):
                    state, action, reward = t.state, t.action, t.reward
                    episode_reward += reward
                    returns[state, action] += episode_reward
                    counts[state, action] += 1
        self.update_qtable(returns, counts)

    def update_qtable(self, returns, counts):
        self.qtable = np.divide(returns,
                                counts,
                                out=np.zeros_like(returns),
                                where=counts != 0)
