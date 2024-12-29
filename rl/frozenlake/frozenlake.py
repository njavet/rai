import gymnasium as gym
from gymnasium.envs.toy_text.frozen_lake import generate_random_map
from pathlib import Path

# project imports
from rl.frozenlake.agents.rmca import RMCAgent
from rl.models import Params


def get_default_params():
    params = Params(total_episodes=2048,
                    alpha=0.8,
                    gamma=0.95,
                    epsilon=0.1,
                    map_size=5,
                    seed=0x101,
                    is_slippery=False,
                    n_runs=16,
                    action_size=4,
                    state_size=25,
                    proba_frozen=0.,
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
    agent = RMCAgent(env, params)
    for episode in range(1024):
        agent.run_episode()
    agent.update()

    print(agent.qtable)
    trajectory = agent.generate_trajectory(learn=False)
    print('number of reached goals:', agent.reached_goal)
    for t in trajectory:
        print(t.state, t.action, t.reward)

