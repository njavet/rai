from pathlib import Path

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
    action_size: int  # Number of possible actions
    state_size: int  # Number of possible states
    proba_frozen: float  # Probability that a tile is frozen
    savefig_folder: Path  # Root folder where plots are saved


params = Params(total_episodes=2000,
                learning_rate=0.8,
                gamma=0.95,
                epsilon=0.1,
                map_size=5,
                seed=123,
                is_slippery=False,
                n_runs=20,
                action_size=None,
                state_size=None,
                proba_frozen=0.9,
                savefig_folder=Path('static/img'))

