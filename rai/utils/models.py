from pydantic import BaseModel, Field


class LearnerParams(BaseModel):
    alpha: float
    gamma: float
    epsilon: float
    epsilon_min: float
    decay: float


class OrchestratorParams(BaseModel):
    n_runs: int
    n_episodes: int
    seed: int


class TrajectoryStep(BaseModel):
    state: int
    action: int
    reward: float
    next_state: int


class Trajectory(BaseModel):
    steps: list[TrajectoryStep] = Field(default_factory=list)
