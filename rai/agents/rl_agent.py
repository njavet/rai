import numpy as np
from collections import defaultdict
from typing import Callable

# project imports
from rai.agents.base import SchopenhauerAgent
from rai.utils.helpers import random_argmax
from rai.utils.models import Params, TrajectoryStep, Trajectory


class RLAgent(SchopenhauerAgent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.vtable = np.zeros(params.state_size)
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.trajectories = defaultdict(list)

    def get_action(self, state: int) -> int:
        action = random_argmax(self.qtable[state])
        return action

    def exec_step(self, state: int, action: int) -> tuple[int, TrajectoryStep, bool]:
        next_state, reward, term, trunc, info = self.env.step(action)
        ts = TrajectoryStep(state=state, action=int(action), reward=reward)
        done = term or trunc
        return next_state, ts, done

    def process_step(self):
        pass

    def generate_trajectory(self) -> Trajectory:
        trajectory = Trajectory(steps=[])
        state, info = self.env.reset()
        done = False
        while not done:
            action = self.get_action(state)
            next_state, ts, done = self.exec_step(state, action)
            state = next_state
            trajectory.steps.append(ts)
            self.process_step()
        return trajectory

    def run_env(self):
        pass



    def run(self):
        qtables = np.zeros((self.params.n_runs,
                            self.params.state_size,
                            self.params.action_size))
        for n in range(self.params.n_runs):
            self.reset_tables()
            for episode in range(self.params.total_episodes):
                trajectory = self.generate_trajectory(self.get_action)
                self.trajectories[episode].append(trajectory)
            qtables[n, :, :] = self.qtable
        self.qtable = qtables.mean(axis=0)


class Learner(RLAgent):
    def __init__(self, env, params):
        super().__init__(env, params)

    def get_action(self, state: int) -> int:
        raise NotImplementedError
