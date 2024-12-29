
from grid.environment import Grid
from grid.agent import Agent


def main():
    env = Grid()
    agent = Agent(env)
    trajectory = agent.run()
    return trajectory

