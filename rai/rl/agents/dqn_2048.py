import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque


class DQLAgent:
    def __init__(self):
        self.model = self.create_model()
        self.target_model = self.create_model()
        self.target_model.load_state_dict(self.model.state_dict())
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.1
        self.batch_size = 64
        self.update_target_steps = 10
        self.steps = 0
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()

    def create_model(self):
        return nn.Sequential(
          nn.Linear(256, 128),
          nn.ReLU(),
          nn.Linear(128, 128),
          nn.ReLU(),
          nn.Linear(128, 4)
        )

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randint(0, 3)
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state)
        return torch.argmax(q_values).item()

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        batch = random.sample(self.memory, self.batch_size)
        states, targets = [], []
        for state, action, reward, next_state, done in batch:
            state_tensor = torch.FloatTensor(state)
            next_state_tensor = torch.FloatTensor(next_state)
            target = self.model(state_tensor.unsqueeze(0)).detach().clone()
            if done:
                target[0][action] = reward
            else:
                next_q_values = self.target_model(next_state_tensor.unsqueeze(0)).detach()
                target[0][action] = reward + self.gamma * torch.max(next_q_values).item()
            states.append(state_tensor)
            targets.append(target[0])

        states = torch.stack(states)
        targets = torch.stack(targets)

        self.optimizer.zero_grad()
        predictions = self.model(states)
        loss = self.criterion(predictions, targets)
        loss.backward()
        self.optimizer.step()

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
