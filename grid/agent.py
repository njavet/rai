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
        all_trajectories = []

        def helper(state_t, action_t, traj_t):
            for action_t1 in Action:
                cond0 = not self.is_inverse_action(action_t, action_t1)
                cond1 = self.is_valid_action(action_t1)
                if cond0 and cond1:
                    new_traj = Trajectory(elements=traj_t.elements)
                    print(new_traj.elements)
                    state_t1 = self.transition(action)
                    reward = self.reward(state_t, action, state_t1)
                    traj_elem_t = TrajectoryElement(state=state_t,
                                                    reward=reward,
                                                    action=action_t)
                    new_traj.elements += (traj_elem_t, )
                    self.state = state_t1
                    if state_t1.x == 2 and state_t1.y == 4:
                        traj_elem_t1 = TrajectoryElement(state=state_t1,
                                                         reward=reward,
                                                         action=None)
                        new_traj.elements += (traj_elem_t1, )
                        all_trajectories.append(new_traj)
                    else:
                        helper(state_t1, action_t1, new_traj)

        for action in Action:
            if self.is_valid_action(action):
                traj_elem = TrajectoryElement(state=self.state,
                                              reward=-1,
                                              action=action)
                traj = Trajectory(elements=(traj_elem,))
                self.state = self.transition(action)
                helper(self.state, action, traj)

        for t in all_trajectories:
            print('traj')
            for elem in t.elements:
                print(elem.state)

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
        if new_state.x < 0 or new_state.x > 4:
            return False
        if new_state.y < 0 or new_state.y > 4:
            return False
        if self.model[new_state.x][new_state.y] == 0:
            return False
        if new_state.y < self.state.y:
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

