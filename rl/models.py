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
    proba_frozen: float
    savefig_folder: Path
    action_size: int | None
    state_size: int | None


class Trajectory(BaseModel):
    state: int
    action: int
    reward: float

