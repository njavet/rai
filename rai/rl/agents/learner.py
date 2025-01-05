from abc import ABC
import torch

# project imports
from rla2048.schemas import LearnerParams, Trajectory


class Learner(ABC):
    def __init__(self, params: LearnerParams, model=None):
        self.params = params
        self.model = model
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
