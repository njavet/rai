from abc import ABC
from pydantic import BaseModel


class Trajectory(BaseModel):
    state: int
    action: int
    reward: float


class Agent(ABC):
    def __init__(self, env):
        self.env = env

    def get_action(self, state):
        raise NotImplementedError

    def policy(self, state):
        raise NotImplementedError
