import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import matplotlib.pyplot as plt

# project imports
from rai.rl.agents.mc import MonteCarlo
from rai.rl.agents.qla import QAgent
from rai.utils.helpers import plot_q_values_map


def get_env(params):
    env = gym.make('FrozenLake-v1',
                   is_slippery=params['is_slippery'],
                   render_mode=params['render_mode'],
                   desc=generate_random_map(size=params['map_size'],
                                            p=params['proba_frozen'],
                                            seed=params['seed']))
    return env


def train_and_show(agent, env, map_size):
    agent.learn(n_runs=4, n_episodes=100000)
    fig = plot_q_values_map(agent.qtable, env, map_size)
    fig.show()


def frozenlake():
    params = {'is_slippery': True,
              'proba_frozen': 0.65,
              'seed': 0x101,
              'map_size': 8,
              'render_mode': 'rgb_array'}
    env = get_env(params)

    mcfv = MonteCarlo(env,
                      gamma=0.85,
                      epsilon=1,
                      epsilon_min=0.01,
                      decay=0.995,
                      fv=True)
    # train_and_show(mcfv, env, params['map_size'])
    tda = QAgent(env,
                 alpha=0.2,
                 gamma=0.9,
                 epsilon=1,
                 epsilon_min=0.01,
                 decay=0.995)
    train_and_show(tda, env, params['map_size'])
    plt.show()
    return

    mcev = MonteCarlo(env,
                      n_runs=16,
                      n_episodes=1024,
                      gamma=0.99,
                      epsilon=1,
                      epsilon_min=0.05,
                      decay=0.99,
                      fv=False)
    mcev.learn()
    print('mcev agent done...')
    fig = plot_q_values_map(mcev.qtable, env, params['map_size'])
    fig.show()
    plt.show()

    # fig.savefig(params.savefig_folder / img_title, bbox_inches="tight")
    # plt.imshow(env.render())
    # plt.axis('off')
    # plt.show()
