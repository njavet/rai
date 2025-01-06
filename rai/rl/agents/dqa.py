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
        self.memory = ReplayMemory(capacity=memory_size)
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.batch_size = batch_size
        self.target_update_steps = target_update_steps
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay = decay

    def epsilon_decay(self):
        self.epsilon = max(self.epsilon * self.decay, self.min_epsilon)

    def process_step(self):
        if len(self.memory) < self.batch_size:
            return
        self.memory.push(self.trajectory[-1])
        batch = self.memory.sample(self.batch_size)


        states, action, rewards, next_states, dones =
        q_values = self.policy_net(states).gather(1, actions)

    def process_episode(self, episode):
        pass

    def learn(self):
        pass


class ReplayMemory:
    def __init__(self, capacity: int):
        self.memory = deque(maxlen=capacity)

    def push(self, *args):
        self.memory.append(args)

    def sample(self, batch_size):
        batch = random.sample(self.memory, batch_size)
        ts for ts in batch
        ts.state

    def __len__(self):
        return len(self.memory)
