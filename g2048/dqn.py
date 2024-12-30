import itertools
import math
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import collections
import random

Transition = collections.namedtuple('Transition',
                                    ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = collections.deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


# Q-network
class DQN(nn.Module):
    def __init__(self, n_observations=16, n_actions=4):
        super().__init__()
        self.layer0 = nn.Linear(n_observations, 128)
        self.layer1 = nn.Linear(128, 128)
        self.layer2 = nn.Linear(128, n_actions)

    def forward(self, x):
        #print('input', x.shape)
        x = F.relu(self.layer0(x))
        #print('layer0', x.shape)
        x = F.relu(self.layer1(x))
        #print('layer1', x.shape)
        x = self.layer2(x)
        #print('output', x.shape)
        return x
        #return self.layer2(x)


def optimize_model(memory,
                   BATCH_SIZE,
                   GAMMA,
                   device,
                   policy_net,
                   target_net,
                   optimizer):
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    #print('batch state', batch.state)
    state_batch = torch.cat(batch.state)
    #print('state', state_batch.shape)
    action_batch = torch.cat(batch.action)
    #print('action', action_batch.shape)
    reward_batch = torch.cat(batch.reward)
    #print('reward', reward_batch.shape)

    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net

    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1).values
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1).values
    # Compute the expected Q values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()


class ConvBlock(nn.Module):
    def __init__(self, idim, odim):
        super().__init__()
        d = odim // 4
        self.conv0 = nn.Conv2d(idim, d, 1, padding='same')
        self.conv1 = nn.Conv2d(idim, d, 2, padding='same')
        self.conv2 = nn.Conv2d(idim, d, 3, padding='same')
        self.conv3 = nn.Conv2d(idim, d, 4, padding='same')

    def forward(self, x):
        x0 = self.conv0(x)
        x1 = self.conv1(x0)
        x2 = self.conv2(x1)
        x3 = self.conv3(x2)
        return torch.cat((x0, x1, x2, x3), dim=1)


class NDQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv0 = ConvBlock(16, 2048)
        self.conv1 = ConvBlock(2048, 2048)
        self.conv2 = ConvBlock(2048, 2048)
        self.dense0 = nn.Linear(2048 * 16, 1024)
        self.dense1 = nn.Linear(1024, 4)

    def forward(self, x):
        x = F.relu(self.conv0(x))
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = nn.Flatten()(x)
        x = F.dropout(self.dense0(x))
        return self.dense1(x)
