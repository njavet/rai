import torch.nn as nn
import torch.nn.functional as F


class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(DQN, self).__init__()
        self.fc0 = nn.Linear(state_dim, 128)
        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, action_dim)

    def forward(self, x):
        x0 = F.relu(self.fc0(x))
        x1 = F.relu(self.fc1(x0))
        x2 = F.relu(self.fc2(x1))
        return x2
