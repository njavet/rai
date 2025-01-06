from collections import deque
import random
import gymnasium as gym
import torch
import torch.optim as optim


# project imports
from rai.rl.agents.learner import Learner
from rai.rl.dqn import DQN


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
                 decay: float,
                 lr: float) -> None:
        super().__init__(env, n_runs, n_episodes)
        self.dev = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.obs_dim = env.observation_space.shape[0]
        self.action_dim = env.action_space.n
        self.policy_net = DQN(self.obs_dim, self.action_dim).to(self.dev)
        self.target_net = DQN(self.obs_dim, self.action_dim).to(self.dev)
        self.memory =
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)


class ReplayMemory:
    def __init__(self, capacity: int):
        self.memory = deque(maxlen=capacity)

    def push(self, *args):
        self.memory.append(args)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
