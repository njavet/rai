from pydantic import BaseModel
from pathlib import Path


class Params(BaseModel):
    total_episodes: int
    alpha: float
    gamma: float
    epsilon: float
    map_size: int
    seed: int
    is_slippery: bool
    n_runs: int
    action_size: int
    state_size: int
    proba_frozen: float
    savefig_folder: Path


class Trajectory(BaseModel):
    state: int
    action: int
    reward: float

