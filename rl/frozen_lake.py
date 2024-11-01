from pathlib import Path
from typing import NamedTuple
from tqdm import tqdm
import seaborn as sns
import gymnasium as gym
import numpy as np
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

# project imports
from rl.config import get_params
from rl.q_learning import get_q_learner
from rl.eps_greedy import EpsilonGreedy


def get_env(params):
    # The frozen lake environment
    env = gym.make(
        'FrozenLake-v1',
        is_slippery=params.is_slippery,
        render_mode='rgb_array',
        desc=generate_random_map(size=params.map_size,
                                 p=params.proba_frozen,
                                 seed=params.seed),
    )
    return env


def init_run(env, params):
    rewards = np.zeros((params.total_episodes, params.n_runs))
    steps = np.zeros((params.total_episodes, params.n_runs))
    episodes = np.arange(params.total_episodes)
    qtables = np.zeros((params.n_runs, env.observation_space.n, env.action_space.n))
    return rewards, steps, episodes, qtables


def run_env_no_learning(env, learner, explorer, params):
    rewards, steps, episodes, qtables = init_run(env, params)
    all_states = []
    all_actions = []

    # Run several times to account for stochasticity
    for run in range(params.n_runs):
        desc = f'Run {run}/{params.n_runs} - Episodes'
        for episode in tqdm(episodes, desc=desc, leave=False):
            state = env.reset(seed=params.seed)[0]
            step = 0
            done = False
            total_rewards = 0

            while not done:
                action = explorer.choose_action(action_space=env.action_space,
                                                state=state,
                                                qtable=learner.qtable)

                # Log all states and actions
                all_states.append(state)
                all_actions.append(action)

                # Take the action (a) and observe the outcome state(s') and reward (r)
                new_state, reward, terminated, truncated, info = env.step(action)

                done = terminated or truncated

                total_rewards += reward
                step += 1

                # Our new state is state
                state = new_state

            # Log all rewards and steps
            rewards[episode, run] = total_rewards
            steps[episode, run] = step
        qtables[run, :, :] = learner.qtable

    return rewards, steps, episodes, qtables, all_states, all_actions


def run_env(env, learner, explorer, params):
    rewards, steps, episodes, qtables = init_run(env, params)
    all_states = []
    all_actions = []

    for run in range(params.n_runs):  # Run several times to account for stochasticity
        learner.reset_qtable()  # Reset the Q-table between runs
        desc = f'Run {run}/{params.n_runs} - Episodes'
        for episode in tqdm(episodes, desc=desc, leave=False):
            state = env.reset(seed=params.seed)[0]
            step = 0
            done = False
            total_rewards = 0

            while not done:
                action = explorer.choose_action(action_space=env.action_space,
                                                state=state,
                                                qtable=learner.qtable)

                # Log all states and actions
                all_states.append(state)
                all_actions.append(action)

                # Take the action (a) and observe the outcome state(s') and reward (r)
                new_state, reward, terminated, truncated, info = env.step(action)

                done = terminated or truncated

                learner.qtable[state, action] = learner.update(
                    state, action, reward, new_state
                )

                total_rewards += reward
                step += 1

                # Our new state is state
                state = new_state

            # Log all rewards and steps
            rewards[episode, run] = total_rewards
            steps[episode, run] = step
        qtables[run, :, :] = learner.qtable

    return rewards, steps, episodes, qtables, all_states, all_actions


def main():
    sns.set_theme()

    params = get_params()
    rng = np.random.default_rng(params.seed)
    env = get_env(params)
    learner = get_q_learner(params, env.action_space.n, env.observation_space.n)
    explorer = EpsilonGreedy(epsilon=params.epsilon, )
    run_env_no_learning(env, learner, explorer, params)
    run_env(env, learner, explorer, params)


if __name__ == '__main__':
    main()
