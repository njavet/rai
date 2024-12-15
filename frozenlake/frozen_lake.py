import seaborn as sns
import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import time

# project imports
from rl.config import get_params
from rl.q_learning import Qlearning
from rl.policy import MonteCarloRandomPolicy, MonteCarloIncPolicy
from rl import misc


def get_env(params):
    env = gym.make(
        'FrozenLake-v1',
        is_slippery=params.is_slippery,
        render_mode="rgb_array",
        desc=generate_random_map(size=params.map_size,
                                 p=params.proba_frozen,
                                 seed=params.seed),)

    return env


def main():
    sns.set_theme()

    params = get_params()
    env = get_env(params)

    # TODO refactor
    # monte carlo random
    t0 = time.time()
    mc_rand = MonteCarloRandomPolicy(env, params)
    rewards, steps, episodes, qtables, states, actions = mc_rand.run()
    print('MC random execution time:', time.time() - t0)

    res, st = misc.postprocess(episodes, params, rewards, steps, params.map_size)
    qtable = qtables.mean(axis=0)  # Average the Q-table between runs
    misc.plot_q_values_map(qtable, env, params.map_size, params, img_label='mc_rand')

    # Plot the state and action distribution
    misc.plot_states_actions_distribution(states=states,
                                          actions=actions,
                                          map_size=params.map_size,
                                          params=params,
                                          img_label='mc_rand')
    misc.plot_steps_and_rewards(res, st, params, 'mc_rand')

    # monte carlo incremental
    t1 = time.time()
    mc_inc = MonteCarloIncPolicy(env, params)
    rewards, steps, episodes, qtables, states, actions = mc_inc.run()
    print('MC incremental execution time:', time.time() - t1)
    res, st = misc.postprocess(episodes, params, rewards, steps, params.map_size)
    qtable = qtables.mean(axis=0)  # Average the Q-table between runs
    misc.plot_q_values_map(qtable, env, params.map_size, params, img_label='mc_inc')

    # Plot the state and action distribution
    misc.plot_states_actions_distribution(states=states,
                                          actions=actions,
                                          map_size=params.map_size,
                                          params=params,
                                          img_label='mc_inc')
    misc.plot_steps_and_rewards(res, st, params, 'mc_inc')

    # Q learning
    t2 = time.time()
    ql = Qlearning(env, params)
    rewards, steps, episodes, qtables, states, actions = ql.q_learning_algorithm()
    print('Q-learning execution time:', time.time() - t2)
    res, st = misc.postprocess(episodes, params, rewards, steps, params.map_size)
    qtable = qtables.mean(axis=0)  # Average the Q-table between runs
    misc.plot_q_values_map(qtable, env, params.map_size, params, img_label='ql')

    # Plot the state and action distribution
    misc.plot_states_actions_distribution(states=states,
                                          actions=actions,
                                          map_size=params.map_size,
                                          params=params,
                                          img_label='ql')
    misc.plot_steps_and_rewards(res, st, params, 'ql')


if __name__ == '__main__':
    main()
