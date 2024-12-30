import numpy as np

# project imports
from rl.models import GymTrajectory


class Agent:
    def __init__(self, env, params):
        self.env = env
        self.params = params


