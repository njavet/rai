import numpy as np
from collections import defaultdict

# project imports
from rai.rl.agents.schopenhauer import SchopenhauerAgent


class Learner(SchopenhauerAgent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.trajectories = defaultdict(list)

    def learn(self):
        raise NotImplementedError
