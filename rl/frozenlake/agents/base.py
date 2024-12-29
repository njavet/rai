from abc import ABC
import gymnasium as gym

# project imports
from rl.models import Params, Trajectory


class Agent(ABC):
    def __init__(self, env: gym.Env, params: Params):
        self.env = env
        self.params = params

    def get_action(self, state, learning):
        raise NotImplementedError

    def update_qtable(self, state, action, reward, next_state):
        pass

    def generate_trajectory(self, learning):
        trajectory = []
        state, info = self.env.reset()
        done = False
        while not done:
            action = self.get_action(state, learning)
            next_state, reward, term, trunc, info = self.env.step(action)
            ts = Trajectory(state=state, action=int(action), reward=reward)
            trajectory.append(ts)
            done = term or trunc
            if learning:
                self.update_qtable(state, action, reward, next_state)
            state = next_state
        return trajectory
