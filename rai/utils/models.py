from pydantic import BaseModel, Field


class TrajectoryStep(BaseModel):
    state: int
    action: int
    reward: float
    next_state: int


class Trajectory(BaseModel):
    steps: list[TrajectoryStep] = Field(default_factory=list)
