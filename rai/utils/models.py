from pydantic import BaseModel, Field
import numpy as np
import torch


class TrajectoryStep(BaseModel):
    # TODO validate that all properties are of the same type
    state: int | np.ndarray | torch.tensor
    action: int | np.ndarray | torch.tensor
    reward: float | np.ndarray | torch.tensor
    next_state: int | np.ndarray | torch.tensor
    done: bool | np.ndarray | torch.tensor

    class Config:
        arbitrary_types_allowed = True


class Trajectory(BaseModel):
    steps: list[TrajectoryStep] = Field(default_factory=list)
