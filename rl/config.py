from pathlib import Path
from typing import NamedTuple

# If is slippery is true the player will move in intended direction with
# probability of 1/3 else will move in either perpendicular direction with
# equal probability of 1/3 in both directions


class Params(NamedTuple):
    total_episodes: int  # Total episodes
    learning_rate: float  # Learning rate
    gamma: float  # Discounting rate
    epsilon: float  # Exploration probability
    map_size: int  # Number of tiles of one side of the squared environment
    seed: int  # Define a seed so that we get reproducible results
    is_slippery: bool
    n_runs: int  # Number of runs
    proba_frozen: float  # Probability that a tile is frozen
    savefig_folder: Path  # Root folder where plots are saved


def get_params():
    params = Params(total_episodes=2000,
                    learning_rate=0.1,
                    gamma=0.98,
                    epsilon=0.2,
                    map_size=4,
                    seed=0x101,
                    is_slippery=True,
                    n_runs=20,
                    proba_frozen=0.9,
                    savefig_folder=Path('rl/static/img'))

    # Create the figure folder if it doesn't exist
    params.savefig_folder.mkdir(parents=True, exist_ok=True)
    return params
