from pathlib import Path
import matplotlib.pyplot as plt
import gymnasium as gym

from rai.rl.envs.wumpus import DungeonEnv
from rai.rl.agents.ql import QLearner
from rai.utils.models import Params
from rai.utils.helpers import plot_q_values_map


def get_default_params():
    params = Params(total_episodes=2**14,
                    alpha=0.1,
                    gamma=0.99,
                    epsilon=0.8,
                    epsilon_min=0.05,
                    decay=0.99,
                    map_size=4,
                    seed=0x101,
                    is_slippery=True,
                    n_runs=32,
                    action_size=4,
                    state_size=16,
                    proba_frozen=0.75,
                    savefig_folder=Path('rl', 'figs'))
    return params


env = DungeonEnv()
params = get_default_params()
ql = QLearner(env, params)

ql.learn()
ql.eps = 0
ql.eps_min = 0
ql.generate_trajectory()
env.render()

print(ql.qtable)
