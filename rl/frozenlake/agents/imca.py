import numpy as np

# project imports
from rl.frozenlake.agents.base import Agent


class IMCAgent(Agent):
    def __init__(self, env, params):
        super().__init__(env, params)
