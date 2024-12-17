import seaborn as sns
import gymnasium as gym
import numpy as np
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import time

# project imports
from frozenlake.config import get_params
from frozenlake import helpers
from frozenlake.rmc import run


def get_env(params):
    env = gym.make(
        'FrozenLake-v1',
        is_slippery=params.is_slippery,
        render_mode="rgb_array",
        desc=generate_random_map(size=params.map_size,
                                 p=params.proba_frozen,
                                 seed=params.seed))

    return env


def main():
    sns.set_theme()

    params = get_params()
    env = get_env(params)

    trajectories = run(env, params)
    for i, trajectory in enumerate(trajectories):
        print('trajectory', i)
        for state, reward, action in trajectory:
            print('state', state, 'reward', reward, 'action', action)
        print(78*'-')


if __name__ == '__main__':
    main()
