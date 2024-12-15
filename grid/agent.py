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
    action: Action | None


class Trajectory(BaseModel):
    elements: tuple


class Agent:
    def __init__(self):
        self.state = State(x=3, y=0)
        self.model = [[1, 1, 1, 1, 1],
                      [1, 0, 1, 1, 1],
                      [1, 0, 1, 0, 1],
                      [1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1]]
        self.gamma = 1

    def generate_trajectories(self):

        def helper(state, action_t=None, traj=None):
            print(traj)
            if traj is None:
                traj = []
            for action in Action:
                cond0 = not self.is_inverse_action(action, action_t)
                cond1 = self.is_valid_action(action)
                if cond0 and cond1:
                    at = traj[:]
                    new_state = self.transition(action)
                    reward = self.reward(state, action, new_state)
                    traj_elem = TrajectoryElement(state=state,
                                                  reward=reward,
                                                  action=action)
                    at.append(traj_elem)
                    if new_state.x == 2 and new_state.y == 4:
                        traj_elem = TrajectoryElement(state=new_state,
                                                      reward=reward)
                        at.append(traj_elem)
                        return at
                    else:
                        return helper(new_state, action, at)
                else:
                    if state.x == 2 and state.y == 4:
                        return traj

        lst = []
        helper(self.state, traj=lst)
        print(lst)

    def is_terminal_state(self):
        return self.state.x == 2 and self.state.y == 4

    def transition(self, action):
        ax, ay = action.value
        xs = self.state.x + ax
        ys = self.state.y + ay
        return State(x=xs, y=ys)

    @staticmethod
    def is_inverse_action(action0, action1=None):
        if action1 is None:
            return False

        ax0, ay0 = action0.value
        ax1, ay1 = action1.value
        return sum([ax0, ay0, ax1, ay1]) == 0

    def is_valid_action(self, action):
        new_state = self.transition(action)
        if new_state.x < 0 or new_state.y > 5:
            return False
        if new_state.y < 0 or new_state.y > 5:
            return False
        if self.model[new_state.x][new_state.y] == 0:
            return False
        return True

    @staticmethod
    def reward(state, action, next_state):
        return -1

    def policy(self):
        pass

    def value_function(self):
        pass

    def q(self, action):
        pass

