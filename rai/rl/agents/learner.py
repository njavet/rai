import gymnasium as gym

# project imports
from rai.rl.agents.schopenhauer import SchopenhauerAgent
from rai.utils.models import Trajectory


class Learner(SchopenhauerAgent):
    def __init__(self, env: gym.Env, params=None):
        super().__init__(env, params)

    def learn(self):
        raise NotImplementedError
