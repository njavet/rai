import random
from collections import deque
import torch
import torch.nn.functional as F
from torch.optim import Adam

# project imports
from rai.rl.dqn import DQN


class Agent:
    def __init__(self,
                 state_dim: int,
                 action_dim: int,
                 lr: float,
                 capacity: int,
                 batch_size: int):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.policy_net = DQN(state_dim, action_dim)
        self.target_net = DQN(state_dim, action_dim)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = Adam(self.policy_net.parameters(), lr=lr)
        self.memory = ReplayMemory(capacity=capacity)
        self.epsilon = 1.0
        self.eps_min = 0.05
        self.decay = 0.995
        self.gamma = 0.99
        self.batch_size = batch_size
        self.steps = 0

    def optimal_policy(self, state):
        with torch.no_grad():
            return self.target_net(torch.FloatTensor(state)).argmax().item()

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        else:
            with torch.no_grad():
                return self.policy_net(torch.FloatTensor(state)).argmax().item()

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return

        batch = self.memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)

        q_values = self.policy_net(states).gather(1, actions)
        next_q_values = self.target_net(next_states).max(1)[0].detach()
        expected_q_values = rewards + (self.gamma * next_q_values * (1 - dones))

        loss = F.mse_loss(q_values.squeeze(), expected_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def epsilon_decay(self):
        self.epsilon = max(self.eps_min, self.decay * self.epsilon)


class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, *args):
        self.memory.append(args)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
