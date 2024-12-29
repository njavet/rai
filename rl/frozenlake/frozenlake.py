import gymnasium as gym

# project imports
from rl.frozenlake.agents.rmca import RMCAgent


def main():
    env = gym.make('FrozenLake-v1', desc=None, map_name='4x4', is_slippery=False)
    agent = RMCAgent(env)
    for episode in range(1024):
        agent.run_episode()
    agent.update()

    print(agent.qtable)
    trajectory = agent.generate_trajectory(learn=False)
    print('number of reached goals:', agent.reached_goal)
    for t in trajectory:
        print(t.state, t.action, t.reward)

