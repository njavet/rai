from abc import ABC
import gymnasium as gym
import numpy as np

# project imports
from rl.models import Params, GymTrajectory


class Agent(ABC):
    def __init__(self, env: gym.Env, params: Params):
        self.env = env
        self.params = params
        self.state_value = np.zeros(params.state_size)
        self.qtable = np.zeros((params.state_size, params.action_size))

    def reset(self):
        self.state_value = np.zeros(self.params.state_size)
        self.qtable = np.zeros((self.params.state_size, self.params.action_size))

    def get_action(self, state):
        raise NotImplementedError

    def get_optimal_action(self, state):
        raise NotImplementedError

    def make_step(self, state, action):
        next_state, reward, term, trunc, info = self.env.step(action)
        ts = GymTrajectory(state=state, action=int(action), reward=reward)
        done = term or trunc
        return next_state, ts, done

    def update_qtable(self, state, action, reward, next_state):
        pass

    @staticmethod
    def random_argmax(arr):
        arr_max = np.max(arr)
        return np.random.choice(np.where(arr == arr_max)[0])

    def generate_trajectory(self, action_selector):
        trajectory = []
        state, info = self.env.reset()
        done = False
        while not done:
            action = action_selector(state)
            next_state, ts, done = self.make_step(state, action)
            state = next_state
            trajectory.append(ts)
        return trajectory

    def run_episode(self, learning=True):
        raise NotImplementedError
