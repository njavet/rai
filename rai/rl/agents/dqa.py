import gymnasium as gym

# project imports
from rai.rl.agents.learner import Learner


class DQNAgent(Learner):
    def __init__(self,
                 env: gym.Env,
                 n_runs: int,
                 n_episodes: int,
                 memory_size: int,
                 batch_size: int,
                 target_update_steps: int,
                 gamma: float,
                 epsilon: float,
                 min_epsilon: float,
                 decay: float) -> None:
        super().__init__(env, n_runs, n_episodes)
