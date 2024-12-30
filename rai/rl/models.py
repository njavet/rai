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


class GymTrajectory(BaseModel):
    state: int
    action: int
    reward: float


class Action(Enum):
    # finite set of actions
    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3


class Trajectory(BaseModel):
    state: tuple[int, int]
    action: Action
    reward: float
