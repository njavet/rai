import torch.nn as nn

class DQN(nn.Module):
    def __init__(self, obs_dim, action_dim):
        super(DQN, self).__init__()
        self.fc0 = nn.Linear(obs_dim, 128)
        self.fc1 = nn.Linear(128, 128)
        self.fc2 = nn.Linear(128, action_dim)

    def forward(self, x):
        x = nn.functional.relu(self.fc0(x))
        x = nn.functional.relu(self.fc1(x))
        return self.fc2(x)

