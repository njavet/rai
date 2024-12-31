import seaborn as sns
import gymnasium as gym
import numpy as np
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
import time

# project imports
from frozenlake.config import get_params
from frozenlake import helpers
from frozenlake.policy import (choose_random_action,
                               choose_eps_greedy,
                               update_qtable)


def get_env(params):
    env = gym.make(
        'FrozenLake-v1',
        is_slippery=params.is_slippery,
        render_mode="rgb_array",
        desc=generate_random_map(size=params.map_size,
                                 p=params.proba_frozen,
                                 seed=params.seed))

    return env


def run(env, params):
    qtables = np.zeros((params.n_runs, env.observation_space.n, env.action_space.n))

        rewards = np.zeros((self.params.total_episodes, self.params.n_runs))
        steps = np.zeros((self.params.total_episodes, self.params.n_runs))
        episodes = np.arange(self.params.total_episodes)
        all_states = []
        all_actions = []

        for i in range(self.params.n_runs):
            for episode in range(self.params.total_episodes):
                done = False
                state, info = self.env.reset()
                total_steps = 0
                total_rewards = 0
                while not done:
                    action = self.choose_action(state)
                    next_state, reward, term, trunc, info = self.env.step(action)

                    # update and collect
                    all_actions.append(action)
                    all_states.append(state)
                    total_rewards += reward
                    total_steps += 1
                    self.trajectories[i].append((state, reward, action))
                    self.update_qtable( state, reward, action)

                    done = term or trunc
                self.update_qtable( next_state, total_rewards, action)
            rewards[episode, i] = total_rewards
            steps[episode, i] = steps
            self.qtables[i, :, :] = self.qtable
        return self.qtables.mean(axis=0), total_steps, rewards, episodes, all_actions, all_states


def main():
    sns.set_theme()

    params = get_params()
    env = get_env(params)

    # monte carlo random
    t0 = time.time()
    mc_rand = MonteCarloRandom(env, params)
    qtable, steps, rewards, episodes, actions, states = mc_rand.run()
    print(qtable)
    print('MC random execution time:', time.time() - t0)
    res, st = helpers.postprocess(episodes, params, rewards, steps, params.map_size)
    helpers.plot_q_values_map(qtable, env, params.map_size, params, img_label='mc_rand')

    # Plot the state and action distribution
    helpers.plot_states_actions_distribution(states=states,
                                          actions=actions,
                                          map_size=params.map_size,
                                          params=params,
                                          img_label='mc_rand')
    helpers.plot_steps_and_rewards(res, st, params, 'mc_rand')

    return
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
