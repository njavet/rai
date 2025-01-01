from pydantic import BaseModel, Field
from pathlib import Path


class Params(BaseModel):
    total_episodes: int
    alpha: float
    gamma: float
    epsilon: float
    epsilon_min: float
    decay: float
    map_size: int
    seed: int
    is_slippery: bool
    n_runs: int
    proba_frozen: float
    savefig_folder: Path
    action_size: int | None
    state_size: int | None


class TrajectoryStep(BaseModel):
    state: int
    action: int
    reward: float
    next_state: int


class Trajectory(BaseModel):
    steps: list[TrajectoryStep] = Field(default_factory=list)
