from pydantic import BaseModel, Field
import torch


class TrajectoryStep(BaseModel):
    state: int | torch.tensor
    action: int | torch.tensor
    reward: float | torch.tensor
    next_state: int | torch.tensor
    done: bool | torch.tensor

    class Config:
        arbitrary_types_allowed = True


class Trajectory(BaseModel):
    steps: list[TrajectoryStep] = Field(default_factory=list)
