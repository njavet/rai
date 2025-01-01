import numpy as np
from collections import defaultdict

# project imports
from rai.rl.agents.schopenhauer import SchopenhauerAgent
from rai.utils.helpers import random_argmax


class Learner(SchopenhauerAgent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.trajectories = defaultdict(list)

    def learn(self):
        raise NotImplementedError


class MonteCarloLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.gamma = params.gamma
        self.eps = params.epsilon
        self.eps_min = params.epsilon_min
        self.decay = params.decay
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.returns = defaultdict(list)

    def policy(self, state):
        epsilon = max(self.eps_min, self.eps * self.decay)
        if np.random.rand() < epsilon:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

