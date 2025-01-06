import gymnasium as gym
from gymnasium.wrappers import RecordVideo
import numpy as np
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecEnv
import torch

# project imports
from rai.rl.agents.dqa import DQNAgent


def train_agent():
    train_env = make_vec_env('LunarLander-v3', n_envs=8)
    obs_dim = train_env.observation_space.shape[0]
    action_dim = train_env.action_space.n
    episode_rewards = np.zeros(train_env.num_envs)
    max_time_steps = 10000

    agent = DQNAgent(obs_dim,
                     action_dim,
                     memory_size=1000000,
                     batch_size=512,
                     target_update_steps=101,
                     gamma=0.99,
                     epsilon=1.0,
                     min_epsilon=0.01,
                     decay=0.995,
                     lr=0.001)

    states = train_env.reset()
    for step in range(max_time_steps):
        actions = agent.select_actions(states)
        next_states, rewards, dones, infos = train_env.step(actions)
        episode_rewards += rewards
        agent.store_transitions(states, actions, rewards, next_states, dones)
        agent.train()
        states = next_states
        if step % 1000 == 0:
            agent.update_target_net()
    torch.save(agent.target_net.state_dict(), 'lunar_vec.pth')
    return agent


def evaluate():
    agent = train_agent()
    env = gym.make('LunarLander-v3',
                   render_mode='human',
                   continuous=False,
                   gravity=-10)
    state = env.reset()[0]
    done = False
    total_reward = 0
    while not done:
        action = agent.optimal_policy(state)
        next_state, reward, done, _, _ = env.step(action)
        state = next_state
        total_reward += reward

