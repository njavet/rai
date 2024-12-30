import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from pathlib import Path
import matplotlib.pyplot as plt

# project imports
from rl.frozenlake.agents.rmca import RMCAgent
from rl.frozenlake.agents.qla import QAgent
from rl.models import Params


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


def main():
    params = get_default_params()
    env = gym.make('FrozenLake-v1',
                   is_slippery=params.is_slippery,
                   render_mode='rgb_array',
                   desc=generate_random_map(size=params.map_size,
                                            p=params.proba_frozen,
                                            seed=params.seed))
    params.state_size = env.observation_space.n
    params.action_size = env.action_space.n
    rmc_agent = RMCAgent(env, params)
    for episode in range(params.total_episodes):
        rmc_agent.run_episode()
    rmc_agent.update()
    trajectory = rmc_agent.generate_trajectory(rmc_agent.get_optimal_action)
    for t in trajectory:
        print('state', t.state, 'action:', t.action)

    q_agent = QAgent(env, params)
    for episode in range(params.total_episodes):
        q_agent.run_episode()

    trajectory = q_agent.generate_trajectory(q_agent.get_optimal_action)
    print('QL')
    for t in trajectory:
        print('state', t.state, 'action:', t.action)

    plt.imshow(env.render())
    plt.axis('off')
    plt.show()
