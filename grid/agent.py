from enum import Enum


class Agent:
    def __init__(self):
        self.state = None
        self.reward = None

    def policy(self, state, action) -> float:
        return 0.

    def value_function(self, state) -> float:
        return 0.

    def predict_next_state(self, state, action):
        pass

    def predict_next_reward(self, state, action):
        pass


class Action(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

