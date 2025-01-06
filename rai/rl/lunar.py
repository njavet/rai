import gymnasium as gym
from gymnasium.wrappers import RecordVideo
import numpy as np
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecEnv
import torch

# project imports
from rai.rl.agents.dqa import DQNAgent
from rai.rl.dqns import DQN


def train_agent():
    train_env = make_vec_env('LunarLander-v3', n_envs=8)
    obs_dim = train_env.observation_space.shape[0]
    action_dim = train_env.action_space.n
    episode_rewards = np.zeros(train_env.num_envs)
    max_time_steps = 100000

    agent = DQNAgent(obs_dim,
                     action_dim,
                     memory_size=1000000,
                     batch_size=512,
                     target_update_steps=101,
                     gamma=0.99,
                     epsilon=1.0,
                     min_epsilon=0.01,
                     decay=0.9999,
                     lr=0.001)

    states = train_env.reset()
    for step in range(max_time_steps):
        actions = agent.select_actions(states)
        next_states, rewards, dones, infos = train_env.step(actions)
        episode_rewards += rewards
        agent.store_transitions(states, actions, rewards, next_states, dones)
        agent.train()
        states = next_states
        if any(dones):
            current_rewards = [episode_rewards[i] for i in
                               range(len(episode_rewards)) if dones[i]]
            print(f'total rewards: ', np.mean(current_rewards))
            print(f'eps', agent.epsilon)
        if step % 1000 == 0:
            agent.update_target_net()
        if step % 100 == 0:
            print(f'step: {step}, rewards: {np.mean(episode_rewards)}')
    torch.save(agent.target_net.state_dict(), 'lunar_vec.pth')
    return agent


def evaluate():
    env = gym.make('LunarLander-v3', render_mode='human')
    model = DQN(env.observation_space.shape[0], env.action_space.n)
    model.load_state_dict(torch.load('lunar_vec.pth'))
    state, _ = env.reset()
    done = False
    total_reward = 0
    while not done:
        with torch.no_grad():
            state = torch.tensor(state, dtype=torch.float32)
            q_values = model(state)
        action = q_values.argmax().numpy()
        next_state, reward, done, _, _ = env.step(action)
        state = next_state
        total_reward += reward
    print('tot reward', total_reward)
