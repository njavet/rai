from pydantic import BaseModel, Field, model_validator
import torch


class TrajectoryStep(BaseModel):
    # TODO validate that all properties are of the same type
    state: int | torch.tensor
    action: int | torch.tensor
    reward: float | torch.tensor
    next_state: int | torch.tensor
    done: bool | torch.tensor

    class Config:
        arbitrary_types_allowed = True


class Trajectory(BaseModel):
    steps: list[TrajectoryStep] = Field(default_factory=list)
