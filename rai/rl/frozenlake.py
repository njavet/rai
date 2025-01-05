import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import matplotlib.pyplot as plt

# project imports
from rai.rl.agents.dp import DP
from rai.utils.helpers import plot_q_values_map


def get_env(params):
    env = gym.make('FrozenLake-v1',
                   is_slippery=params['is_slippery'],
                   render_mode=params['render_mode'],
                   desc=generate_random_map(size=params['map_size'],
                                            p=params['proba_frozen'],
                                            seed=params['seed']))
    return env


def frozenlake():
    params = {'is_slippery': False,
              'proba_frozen': 0.8,
              'seed': 0x101,
              'map_size': 4,
              'render_mode': 'human'}
    env = get_env(params)
    dp = DP(env.observation_space, env.action_space)

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
