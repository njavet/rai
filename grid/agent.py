from enum import Enum
from pydantic import BaseModel


class State(BaseModel):
    x: int
    y: int


class Action(Enum):
    # finite set of actions
    UP = -1, 0
    RIGHT = 0, 1
    DOWN = 1, 0
    LEFT = 0, -1


class TrajectoryElement(BaseModel):
    state: State
    reward: float
    action: Action


class Agent:
    def __init__(self):
        self.state = 3, 0
        self.terminal_state = 2, 4
        self.model = [[1, 1, 1, 1, 1],
                      [1, 0, 1, 1, 1],
                      [1, 0, 1, 0, 1],
                      [1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1]]
        self.gamma = 1

    def generate_trajectories(self):
        lst = []

        def helper(state_t, action_t, traj):
            for action in Action:
                cond0 = self.is_inverse_action(action, action_t)
                cond1 = self.is_valid_action(action)
                state_t1 =
                if cond0 and cond1:
                    traj.append(state_t)
                    traj.append(self.reward())
                    traj.append(state_t)

    def is_inverse_action(self, action0, action1):
        ax0, ay0 = action0.value
        ax1, ay1 = action1.value
        return sum([ax0, ay0, ax1, ay1]) == 0

    def is_valid_action(self, action):
        ax, ay = action.value
        x, y = self.state
        new_x = ax + x
        new_y = ay + y
        if new_x < 0 or new_x > 5:
            return False
        if new_y < 0 or new_y > 5:
            return False
        if self.model[new_x][new_y] == 0:
            return False
        return True

    @staticmethod
    def reward(state, action, next_state):
        return -1

    def transition(self, action):
        x, y = self.state
        ax, ay = action.value
        xs = self.model[x] + ax
        ys = self.model[x][y] + ay
        self.state = xs, ys

    def policy(self):
        pass

    def value_function(self):
        pass

    def q(self, action):
        pass

