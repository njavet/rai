import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from pathlib import Path
import matplotlib.pyplot as plt

# project imports
from rai.rl.agents.mcev import MonteCarloEV
from rai.rl.agents.mcfv import MonteCarloFV
from rai.rl.agents.ql import QLearner
from rai.rl.agents.q2l import Q2Learner
from rai.utils.helpers import plot_q_values_map
from rai.utils.models import Params


def get_default_params():
    params = Params(total_episodes=2**14,
                    alpha=0.1,
                    gamma=0.99,
                    epsilon=0.8,
                    epsilon_min=0.05,
                    decay=0.99,
                    map_size=5,
                    seed=0x101,
                    is_slippery=True,
                    n_runs=32,
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

    mcev_agent = MonteCarloEV(env, params)
    mcev_agent.learn()
    print('mcev agent done...')
    fig = plot_q_values_map(mcev_agent.qtable, env, params.map_size)
    fig.show()

    mcfv_agent = MonteCarloFV(env, params)
    mcfv_agent.learn()
    print('mcfv agent done...')
    fig = plot_q_values_map(mcfv_agent.qtable, env, params.map_size)
    fig.show()

    q_learner = QLearner(env, params)
    q_learner.learn()
    fig = plot_q_values_map(q_learner.qtable, env, params.map_size)
    fig.show()
    print('q agent done...')

    q2_learner = Q2Learner(env, params)
    q2_learner.learn()
    fig = plot_q_values_map(q2_learner.qtable, env, params.map_size)
    fig.show()
    plt.show()

    # fig.savefig(params.savefig_folder / img_title, bbox_inches="tight")
    # plt.imshow(env.render())
    # plt.axis('off')
    # plt.show()
