import gymnasium as gym

# project imports
from rai.rl.agents.schopenhauer import SchopenhauerAgent


class Learner(SchopenhauerAgent):
    def __init__(self, env: gym.Env, n_runs: int, n_episodes: int):
        super().__init__(env)
        self.n_runs = n_runs
        self.n_episodes = n_episodes

    def epsilon_decay(self):
        raise NotImplementedError

    def learn(self):
        raise NotImplementedError
