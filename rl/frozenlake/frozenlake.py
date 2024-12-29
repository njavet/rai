import gymnasium as gym

# project imports
from rl.frozenlake.agents.rmca import RMCAgent


def main():
    env = gym.make('FrozenLake-v1', desc=None, map_name='4x4')
    agent = RMCAgent(env)
    for episode in range(1024):
        agent.run_episode()
    agent.update()

    print(agent.qtable)
