from abc import ABC
import gymnasium as gym
from collections import defaultdict
from typing import Callable
import numpy as np

# project imports
from rl.models import Params, GymTrajectory


class Agent(ABC):
    def __init__(self, env: gym.Env, params: Params) -> None:
        self.env = env
        self.params = params
        self.vtable = np.zeros(params.state_size)
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.trajectories = defaultdict(list)

    def reset_tables(self) -> None:
        self.vtable = np.zeros(self.params.state_size)
        self.qtable = np.zeros((self.params.state_size, self.params.action_size))

    def get_action(self, state: int) -> int:
        raise NotImplementedError

    def get_optimal_action(self, state: int) -> int:
        action = self.random_argmax(self.qtable[state])
        return action

    def make_step(self, state: int, action: int) -> tuple[int, GymTrajectory, bool]:
        next_state, reward, term, trunc, info = self.env.step(action)
        ts = GymTrajectory(state=state, action=int(action), reward=reward)
        done = term or trunc
        return next_state, ts, done

    @staticmethod
    def random_argmax(arr: np.ndarray) -> int:
        arr_max = np.max(arr)
        arr_maxes = np.where(arr == arr_max)[0]
        action = int(np.random.choice(arr_maxes))
        return action

    def generate_trajectory(self, action_selector: Callable) -> list[GymTrajectory]:
        trajectory = []
        state, info = self.env.reset()
        done = False
        while not done:
            action = action_selector(state)
            next_state, ts, done = self.make_step(state, action)
            state = next_state
            trajectory.append(ts)
        return trajectory

    @staticmethod
    def convert_trajectory(trajectory: list[GymTrajectory]) -> np.ndarray:
        np_traj = np.array([[t.state, t.action, t.reward] for t in trajectory])
        return np_traj

    def run(self):
        qtables = np.zeros((self.params.n_runs,
                            self.params.state_size,
                            self.params.action_size))
        for n in range(self.params.n_runs):
            self.reset_tables()
            for episode in range(self.params.total_episodes):
                trajectory = self.generate_trajectory(self.get_action)
                self.trajectories[(n, episode)] = trajectory
            qtables[n, :, :] = self.qtable
        self.qtable = qtables.mean(axis=0)
