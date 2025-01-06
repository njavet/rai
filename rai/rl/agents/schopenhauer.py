from abc import ABC
import gymnasium as gym
import numpy as np

# project imports
from rai.utils.models import Trajectory, TrajectoryStep


class SchopenhauerAgent(ABC):
    """
    For now lets define a SchopenhauerAgent as an Agent
    that has an environment as part of himself. So the environment exists
    only inside the agent. Another type would be a Cartesian Agent that is
    part of the environment. The third Agent type would be a mix of both.
    """
    def __init__(self, env: gym.Env):
        """ params could be seen as given by nature / god """
        self.env = env
        self.trajectory: Trajectory = Trajectory()

    def policy(self, state):
        raise NotImplementedError

    def reset(self):
        self.trajectory = Trajectory()

    def exec_step(self,
                  state: np.ndarray,
                  action: np.ndarray) -> tuple[TrajectoryStep, bool]:
        next_state, reward, term, trunc, info = self.env.step(action)
        done = term or trunc
        ts = TrajectoryStep(state=np.array(state, dtype=np.float32),
                            action=np.array(action, dtype=np.long),
                            reward=np.array(reward, dtype=np.float32),
                            next_state=np.array(next_state, dtype=np.float32),
                            done=np.array(done, dtype=np.float32))
        return ts, done

    def process_step(self):
        pass

    def generate_trajectory(self, max_iter=None):
        self.reset()
        state, info = self.env.reset()
        done = False
        while not done:
            action = self.policy(state)
            ts, done = self.exec_step(state, action)
            self.trajectory.steps.append(ts)
            self.process_step()
            state = ts.next_state

    def process_episode(self, episode):
        pass
