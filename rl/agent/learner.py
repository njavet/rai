from abc import ABC
import numpy as np

# project imports
from rl.models import GymTrajectory


class Learner(ABC):
    def __init__(self, env, params):
        self.env = env
        self.params = params
        self.value = np.zeros(params.state_size)
        self.qtable = np.zeros((params.state_size, params.action_size))

    def get_action(self, state):
        raise NotImplementedError

    def generate_trajectory(self):
        trajectory = GymTrajectory()
        state, info = self.env.reset()
        done = False
        while not done:
            action = self.get_action(state)
            next_state, reward, term, trunc, info = self.env.step(action)
            trajectory.state.append(state)
            trajectory.action.append(int(action))
            trajectory.reward.append(reward)
            done = term or trunc
            state = next_state
        return trajectory
