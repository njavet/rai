import collections
from rich.text import Text
import gymnasium as gym
from rich.console import Console
import itertools
import math
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import collections

import random
import dqn
import gym_game
import utils2048


BATCH_SIZE = 64
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.01
EPS_DECAY = 1000
TAU = 0.005
LR = 1e-5

episode_durations = []
scores = []
if torch.cuda.is_available():
    num_episodes = 5000

else:
    num_episodes = 50

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


policy_net = dqn.NDQN().to(device)
target_net = dqn.NDQN().to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = dqn.ReplayMemory(50000)

env = gym_game.Env2048()


def select_action(state):
    sample = random.random()
    eps_threshold = 0.1
    # exploitation
    if sample > eps_threshold:
        with torch.no_grad():

            #return policy_net(state).max(1).indices.view(1, 1)
            st = torch.tensor(state.reshape(1, 16), dtype=torch.float32)
            res = policy_net(st)
            return res.reshape(1, 4).max(1).indices.view(1, 1)
    # exploration
    else:
        # return env.action_space.sample()
        return torch.tensor([[env.action_space.sample()]], device=device, dtype=torch.long)


for i_episode in range(num_episodes):
    # Initialize the environment and get it's state
    state, info = env.reset()
    # state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    state = torch.tensor(state.reshape(1, 16), device=device).unsqueeze(0)
    for t in itertools.count():
        action = select_action(state)
        observation, reward, terminated, truncated, _ = env.step(action.item())
        reward = torch.tensor([reward], device=device)
        done = terminated or truncated

        if terminated:
            next_state = None
            scores.append(env.score)
        else:
            next_state = torch.tensor(observation.reshape(16),
                                      dtype=torch.float32,
                                      device=device).unsqueeze(0)

        # Store the transition in memory
        memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        dqn.optimize_model(memory, BATCH_SIZE, GAMMA,
                           device, policy_net, target_net, optimizer)

        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
        target_net_state_dict = target_net.state_dict()
        policy_net_state_dict = policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
        target_net.load_state_dict(target_net_state_dict)

        if done:
            episode_durations.append(t + 1)
            break

min_eps = min(episode_durations)
max_eps = max(episode_durations)
min_sc = min(scores)
max_sc = max(scores)

print('number of games', len(scores))
print('worst score', min_sc, 'best score', max_sc)
print('shortest duration', min_eps, 'longest duraction', max_eps)


torch.save(policy_net.state_dict(), 'policy_state_dict.pth')
torch.save(policy_net, 'policy.pth')
