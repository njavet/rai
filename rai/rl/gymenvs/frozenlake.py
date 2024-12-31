import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from pathlib import Path
import matplotlib.pyplot as plt

# project imports
from rai.rl.agents.mc_learner import MCLearner
from rai.rl.agents.q_learner import QLearner
from rai.utils.helpers import plot_q_values_map
from rai.utils.models import Params


def get_default_params():
    params = Params(total_episodes=4*4096,
                    alpha=0.1,
                    gamma=0.99,
                    epsilon=0.2,
                    map_size=5,
                    seed=0x101,
                    is_slippery=False,
                    n_runs=4*8,
                    action_size=None,
                    state_size=None,
                    proba_frozen=0.75,
                    savefig_folder=Path('rl', 'figs'))
    return params


def get_env(params):
    env = gym.make('FrozenLake-v1',
                   is_slippery=params.is_slippery,
                   render_mode='rgb_array',
                   desc=generate_random_map(size=params.map_size,
                                            p=params.proba_frozen,
                                            seed=params.seed))
    params.state_size = env.observation_space.n
    params.action_size = env.action_space.n
    return env


def frozenlake():
    params = get_default_params()
    env = get_env(params)

    mc_agent = MCLearner(env, params)
    mc_agent.run_env()
    fig = plot_q_values_map(mc_agent.qtable, env, params.map_size)
    fig.show()

    q_learner = QLearner(env, params)
    q_learner.run_env()
    fig = plot_q_values_map(q_learner.qtable, env, params.map_size)
    fig.show()
    plt.show()
    # fig.savefig(params.savefig_folder / img_title, bbox_inches="tight")
    # plt.imshow(env.render())
    # plt.axis('off')
    # plt.show()
