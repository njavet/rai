from pathlib import Path
from typing import NamedTuple
from tqdm import tqdm

import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map

from misc import *

sns.set_theme()

class Params(NamedTuple):
    total_episodes: int  # Total episodes
    learning_rate: float  # Learning rate
    gamma: float  # Discounting rate
    epsilon: float  # Exploration probability
    map_size: int  # Number of tiles of one side of the squared environment
    seed: int  # Define a seed so that we get reproducible results
    is_slippery: bool  # If true120 the player will move in intended direction with probability of 1/3 else will move in either perpendicular direction with equal probability of 1/3 in both directions
    n_runs: int  # Number of runs
    action_size: int  # Number of possible actions
    state_size: int  # Number of possible states
    proba_frozen: float  # Probability that a tile is frozen
    savefig_folder: Path  # Root folder where plots are saved


params = Params(total_episodes=2000,
                learning_rate=0.8,
                gamma=0.95,
                epsilon=0.1,
                map_size=5,
                seed=123,
                is_slippery=False,
                n_runs=20,
                action_size=None,
                state_size=None,
                proba_frozen=0.9,
                savefig_folder=Path("./_static/img"),)


# Set the seed
rng = np.random.default_rng(params.seed)


# Create the figure folder if it doesn't exist
params.savefig_folder.mkdir(parents=True, exist_ok=True)


# The frozen lake environment
env = gym.make(
    "FrozenLake-v1",
    is_slippery=params.is_slippery,
    render_mode="rgb_array",
    desc=generate_random_map(
        size=params.map_size, p=params.proba_frozen, seed=params.seed
    ),
)

params = params._replace(action_size=env.action_space.n)
params = params._replace(state_size=env.observation_space.n)
print(f"Action size: {params.action_size}")
print(f"State size: {params.state_size}")


class Qlearning:
    def __init__(self, learning_rate, gamma, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.reset_qtable()
        self.qtable = np.zeros((self.state_size, self.action_size))


    def update(self, state, action, reward, new_state):
        """TODO: Change the following code to implement the update of the Q-function
            Q_update(s,a):= Q(s,a) + learning_rate * delta
                delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)]"""

        q_update = self.qtable[state, action]
        return q_update

    def reset_qtable(self):
        """Reset the Q-table."""
        self.qtable = np.zeros((self.state_size, self.action_size))


class EpsilonGreedy:
    def __init__(self, epsilon):
        self.epsilon = epsilon

    def choose_action(self, action_space, state, qtable):
        """TODO: Implement the e-greedy algorithm. i.e.:
            with probability epsilon:
                select an action randomly
            else
                select the action with the highest q-value"""

        # Select a random action
        action = action_space.sample()
        return action


learner = Qlearning(learning_rate=params.learning_rate,
                    gamma=params.gamma,
                    state_size=params.state_size,
                    action_size=params.action_size,)

explorer = EpsilonGreedy(epsilon=params.epsilon,)


def run_env_no_learning():
    rewards = np.zeros((params.total_episodes, params.n_runs))
    steps = np.zeros((params.total_episodes, params.n_runs))
    episodes = np.arange(params.total_episodes)
    qtables = np.zeros((params.n_runs, params.state_size, params.action_size))
    all_states = []
    all_actions = []

    for run in range(params.n_runs):  # Run several times to account for stochasticity

        for episode in tqdm(
                episodes, desc=f"Run {run}/{params.n_runs} - Episodes", leave=False
        ):
            state = env.reset(seed=params.seed)[0]  # Reset the environment
            step = 0
            done = False
            total_rewards = 0

            while not done:
                action = explorer.choose_action(
                    action_space=env.action_space, state=state, qtable=learner.qtable
                )

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


all_states = []
all_actions = []

env = gym.make("FrozenLake-v1",
               is_slippery=params.is_slippery,
               render_mode="rgb_array",
               desc=generate_random_map(
                   size=params.map_size, p=params.proba_frozen, seed=params.seed),)

params = params._replace(action_size=env.action_space.n)
params = params._replace(state_size=env.observation_space.n)

# Set the seed to get reproducible results when sampling the action space
env.action_space.seed(params.seed)
learner = Qlearning(learning_rate=params.learning_rate,
                    gamma=params.gamma,
                    state_size=params.state_size,
                    action_size=params.action_size,)

# Force exploration in every step
explorer = EpsilonGreedy(epsilon=1.0,)

state = env.reset(seed=params.seed)[0]  # Reset the environment

# Initialize the Q-table with zero values
learner.reset_qtable()

# Generate several trajectories using the Q-function without exploration and plot
# the distribution of states visited and actions taken

# Notice that if the policy directs the agent towards the border of the
# environment, it will remain stuck at that point

rewards, steps, episodes, qtables, all_states, all_actions = run_env_no_learning()

# Save the results in dataframes
res, st = postprocess(episodes, params, rewards, steps, params.map_size)

# Plot the Q-table
plot_q_values_map(learner.qtable, env, params.map_size, params, img_label='random')

# Plot the state and action distribution
plot_states_actions_distribution(states=all_states,
                                 actions=all_actions,
                                 map_size=params.map_size,
                                 params=params,
                                 img_label='random')

env.close()
plot_steps_and_rewards(res, st, params)


def run_env():
    rewards = np.zeros((params.total_episodes, params.n_runs))
    steps = np.zeros((params.total_episodes, params.n_runs))
    episodes = np.arange(params.total_episodes)
    qtables = np.zeros((params.n_runs, params.state_size, params.action_size))
    all_states = []
    all_actions = []

    for run in range(params.n_runs):  # Run several times to account for stochasticity
        learner.reset_qtable()  # Reset the Q-table between runs

        for episode in tqdm(
            episodes, desc=f"Run {run}/{params.n_runs} - Episodes", leave=False
        ):
            state = env.reset(seed=params.seed)[0]  # Reset the environment
            step = 0
            done = False
            total_rewards = 0

            while not done:
                action = explorer.choose_action(
                    action_space=env.action_space, state=state, qtable=learner.qtable
                )

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


env = gym.make(
    "FrozenLake-v1",
    is_slippery=params.is_slippery,
    render_mode="rgb_array",
    desc=generate_random_map(
        size=params.map_size, p=params.proba_frozen, seed=params.seed
    ),
)

params = params._replace(action_size=env.action_space.n)
params = params._replace(state_size=env.observation_space.n)
env.action_space.seed(
    params.seed
)  # Set the seed to get reproducible results when sampling the action space
learner = Qlearning(learning_rate=params.learning_rate,
                    gamma=params.gamma,
                    state_size=params.state_size,
                    action_size=params.action_size,)
explorer = EpsilonGreedy(epsilon=params.epsilon,)

rewards, steps, episodes, qtables, all_states, all_actions = run_env()

# Save the results in dataframes
res, st = postprocess(episodes, params, rewards, steps, params.map_size)
qtable = qtables.mean(axis=0)  # Average the Q-table between runs

# Plot the Q-table
plot_q_values_map(qtable, env, params.map_size, params=params, img_label='learned')

# Plot the state and action distribution
plot_states_actions_distribution(states=all_states,
                                 actions=all_actions,
                                 map_size=params.map_size,
                                 params=params,
                                 img_label='learned')

env.close()
plot_steps_and_rewards(res, st, params)