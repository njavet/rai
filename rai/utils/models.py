from pydantic import BaseModel, Field
import numpy as np


class TrajectoryStep(BaseModel):
    state: np.ndarray
    action: np.ndarray
    reward: np.ndarray
    next_state: np.ndarray
    done: np.ndarray

    class Config:
        arbitrary_types_allowed = True


class Trajectory(BaseModel):
    steps: list[TrajectoryStep] = Field(default_factory=list)
