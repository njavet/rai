from pydantic import BaseModel
from pathlib import Path
from enum import Enum


class Params(BaseModel):
    total_episodes: int
    alpha: float
    gamma: float
    epsilon: float
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


class Trajectory(BaseModel):
    steps: list[TrajectoryStep]
