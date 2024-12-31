from abc import ABC
import numpy as np
from collections import defaultdict

# project imports
from rai.utils.models import Trajectory, TrajectoryStep


class SchopenhauerAgent(ABC):
    """
    For now lets define a SchopenhauerAgent as an Agent
    that has an environment as part of himself. So the environment exists
    only inside the agent. Another type would be a Cartesian Agent that is
    part of the environment. The third Agent type would be a mix of both.
    """
    def __init__(self, env, params):
        """ params could be seen as given by nature / god """
        self.env = env
        self.params = params
        # every agent has a trajectory (for humans it would be from birth to death)
        self.trajectory = Trajectory()

    def reset(self):
        self.trajectory = Trajectory()

    def policy(self, state: int) -> int:
        raise NotImplementedError

    def exec_step(self, state: int, action: int) -> tuple[int, TrajectoryStep, bool]:
        next_state, reward, term, trunc, info = self.env.step(action)
        ts = TrajectoryStep(state=state, action=int(action), reward=reward)
        done = term or trunc
        return next_state, ts, done

    def process_step(self, next_state):
        pass

    def generate_trajectory(self):
        # self reset
        self.reset()
        state, info = self.env.reset()
        done = False
        while not done:
            action = self.policy(state)
            next_state, ts, done = self.exec_step(state, action)
            self.trajectory.steps.append(ts)
            # the agent might want to do something after each step
            self.process_step(next_state)
            state = next_state

    def process_episode(self, episode):
        pass


class Learner(SchopenhauerAgent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.vtable = np.zeros(params.state_size)
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.trajectories = defaultdict(list)

    def reset_q_table(self):
        self.qtable = np.zeros((self.params.state_size, self.params.action_size))

    def process_episode(self, episode) -> tuple[np.ndarray, np.ndarray]:
        returns = np.zeros((self.params.state_size, self.params.action_size))
        counts = np.zeros((self.params.state_size, self.params.action_size))
        total_reward = 0
        for t in reversed(self.trajectory.steps):
            state, action, reward = t.state, t.action, t.reward
            total_reward += reward
            returns[state, action] += total_reward
            counts[state, action] += 1
        return returns, counts

    def process_episodes(self):
        pass

    def run_env(self):
        qtables = np.zeros((self.params.n_runs,
                            self.params.state_size,
                            self.params.action_size))
        for n in range(self.params.n_runs):
            self.reset_q_table()
            for episode in range(self.params.total_episodes):
                trajectory = self.generate_trajectory()
                self.trajectories[episode].append(trajectory)
                # the agent might want to do something after each episode
                self.process_episode(episode)
            # the agent might want to do something after all episodes
            self.process_episodes()
            qtables[n, :, :] = self.qtable
        self.qtable = qtables.mean(axis=0)
