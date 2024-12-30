import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from pathlib import Path
import matplotlib.pyplot as plt

# project imports
from rai.agents.rmc_learner import RMCLearner
from rai.utils.models import Params


def get_default_params():
    params = Params(total_episodes=2048,
                    alpha=0.8,
                    gamma=0.95,
                    epsilon=0.1,
                    map_size=4,
                    seed=0x101,
                    is_slippery=False,
                    n_runs=16,
                    action_size=None,
                    state_size=None,
                    proba_frozen=0.8,
                    savefig_folder=Path('rl', 'figs'))
    return params


def rmc(env, params):
    for episode in range(params.total_episodes):
        rmc_agent.run_env()
    return rmc_agent


def imc(env, params):
    imc_agent = IMCLearner(env, params)
    for episode in range(params.total_episodes):
        imc_agent.run_env()
    return imc_agent


def qagent(env, params):
    q_agent = QLearner(env, params)
    for episode in range(params.total_episodes):
        q_agent.run_env()
    return q_agent


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


def main():
    params = get_default_params()
    env = get_env(params)
    # random monte carlo agent
    rmc_agent = RMCLearner(env, params)
    rmc_agent.run_env()

    trajectory = rmc_agent.generate_trajectory()
    print('random mc')
    for t in trajectory.steps:
        print('state', t.state, 'action:', t.action)

    return
    # incremental mc
    imc_agent = imc(env, params)
    trajectory = imc_agent.generate_trajectory()
    print('inc mc')
    for t in trajectory.steps:
        print('state', t.state, 'action:', t.action)

    # incremental mc
    q_agent = qagent(env, params)
    trajectory = q_agent.generate_trajectory()
    print('QL')
    for t in trajectory.steps:
        print('state', t.state, 'action:', t.action)

    plt.imshow(env.render())
    plt.axis('off')
    plt.show()
