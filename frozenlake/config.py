from dataclasses import dataclass


class Params(dataclass):
    total_episodes: int  # Total episodes
    alpha: float  # Learning rate
    gamma: float  # Discounting rate
    epsilon: float  # Exploration probability
    map_size: int  # Number of tiles of one side of the squared environment
    seed: int  # Define a seed so that we get reproducible results
    is_slippery: bool
    n_runs: int  # Number of runs
    proba_frozen: float  # Probability that a tile is frozen
    max_episode_steps: int
