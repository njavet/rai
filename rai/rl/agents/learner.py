from abc import ABC
from gymnasium.spaces import Discrete
import torch

# project imports
from rai.utils.models import LearnerParams, Trajectory


class Learner(ABC):
    def __init__(self, params: LearnerParams, action_space: Discrete, model=None):
        self.params = params
        self.model = model
        self.action_space = action_space
        self.trajectory: Trajectory = Trajectory()

    def reset_trajectory(self) -> None:
        self.trajectory = Trajectory()

    def policy(self, state: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError

    def process_step(self) -> None:
        raise NotImplementedError

    def process_episode(self, episode: int) -> None:
        raise NotImplementedError

    def learn(self):
        raise NotImplementedError
