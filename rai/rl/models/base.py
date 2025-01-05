from abc import ABC


class BaseGridModel(ABC):
    def __init__(self, m: int, n: int):
        self.m = m
        self.n = n
        self.state = None

    def obs_to_state(self, obs):
        raise NotImplementedError

    def action_to_op(self, action):
        raise NotImplementedError

    def get_reward(self, state, action) -> float:
        raise NotImplementedError

    def execute_op(self, action):
        raise NotImplementedError
