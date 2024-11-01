import seaborn as sns
import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

# project imports
from rl.config import get_params
from rl.q_learning import Qlearning
from rl.policy import MonteCarloRandomPolicy, MonteCarloIncPolicy
from rl import misc


def get_env(params):
    env = gym.make(
        'FrozenLake-v1',
        is_slippery=params.is_slippery,
        desc=None,
        map_name='4x4')
    return env


def main():
    sns.set_theme()

    params = get_params()
    env = get_env(params)

    #mc_rand = MonteCarloRandomPolicy(env, params)
    #mc_inc = MonteCarloIncPolicy(env, params)
    ql = Qlearning(env, params)

    vf = ql.q_learning_algorithm()
    #misc.plot_q_values_map(ql.qtable, env, params.map_size, params, img_label='ql')
    print(vf)


if __name__ == '__main__':
    main()
