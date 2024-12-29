import gymnasium as gym


def main():
    env = gym.make('FrozenLake-v1', desc=None, map_name='4x4')

