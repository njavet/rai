from pathlib import Path
from typing import NamedTuple
from tqdm import tqdm
import seaborn as sns
import gymnasium as gym
import numpy as np
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

# project imports
from rl.config import get_params
from rl.q_learning import Qlearning
from rl.policy import MonteCarloRandomPolicy, MonteCarloIncPolicy


def get_env(params):
    # The frozen lake environment
    env = gym.make(
        'FrozenLake-v1',
        is_slippery=params.is_slippery,
        render_mode='rgb_array',
        desc=generate_random_map(size=params.map_size,
                                 p=params.proba_frozen,
                                 seed=params.seed),
    )
    return env


def main():
    sns.set_theme()

    params = get_params()
    env = get_env(params)

    mc_rand = MonteCarloRandomPolicy(env, params)
    mc_inc = MonteCarloIncPolicy(env, params)
    ql = Qlearning(env, params)


if __name__ == '__main__':
    main()
