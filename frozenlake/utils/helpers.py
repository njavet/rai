# project imports
from frozenlake.config import Params


def get_params():
    params = Params(total_episodes=4,
                    alpha=0.1,
                    gamma=0.97,
                    epsilon=0.25,
                    map_size=4,
                    seed=101,
                    is_slippery=False,
                    n_runs=4,
                    proba_frozen=1,
                    max_episode_steps=101)

    return params
