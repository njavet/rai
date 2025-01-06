from abc import ABC
import gymnasium as gym
import torch
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
        self.dev = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.trajectory: Trajectory = Trajectory()

    def policy(self, state):
        raise NotImplementedError

    def reset(self):
        self.trajectory = Trajectory()

    def exec_int_step(self, state: int, action: int) -> TrajectoryStep:
        next_state, reward, term, trunc, info = self.env.step(action)
        done = term or trunc
        ts = TrajectoryStep(state=state,
                            action=action,
                            reward=reward,
                            next_state=next_state,
                            done=done)
        return ts

    def exec_tensor_step(self,
                         state: np.ndarray,
                         action: np.int64) -> TrajectoryStep:
        next_state, reward, term, trunc, info = self.env.step(action)
        done = term or trunc
        # convert to torch tensors
        state = torch.tensor(state, dtype=torch.float32, device=self.dev)
        action = torch.tensor(state, dtype=torch.long, device=self.dev)
        reward = torch.tensor(state, dtype=torch.float32, device=self.dev)
        next_state = torch.tensor(next_state, dtype=torch.float32, device=self.dev)
        done = torch.tensor(done, dtype=torch.float32, device=self.dev)
        ts = TrajectoryStep(state=state,
                            action=action,
                            reward=reward,
                            next_state=next_state,
                            done=done)
        return ts

    def process_step(self):
        pass

    def generate_trajectory(self, max_iter=None, dtype=None):
        self.reset()
        state, info = self.env.reset()
        done = False
        while not done:
            action = self.policy(state)
            if dtype is None:
                ts = self.exec_int_step(state, action)
            else:
                ts = self.exec_tensor_step(state, action)
            self.trajectory.steps.append(ts)
            self.process_step()
            state = ts.next_state
            done = ts.done

    def process_episode(self, episode):
        pass
