import numpy as np

# project imports
from rai.rl.agents.base import Learner


class RMCLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)

    def policy(self, state):
        action = self.env.action_space.sample()
        return action

    def process_episodes(self):
        returns = np.zeros((self.params.state_size, self.params.action_size))
        counts = np.zeros((self.params.state_size, self.params.action_size))
        for episode, trajectories in self.trajectories.items():
            for trajectory in trajectories:
                rs, cs = self.process_episode(episode)
                returns += rs
                counts += cs
        self.update_qtable(returns, counts)

    def update_qtable(self, returns, counts):
        self.qtable = np.divide(returns,
                                counts,
                                out=np.zeros_like(returns),
                                where=counts != 0)
