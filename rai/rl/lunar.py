import gymnasium as gym
from gymnasium.wrappers import RecordVideo
import torch

# project imports
from rai.rl.agents.dqa import DQNAgent


def train_agent():
    train_env = gym.make('LunarLander-v3')
    obs_dim = train_env.observation_space.shape[0]
    action_dim = train_env.action_space.n

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

    for episode in range(1000):
        state = env.reset()[0]
        total_reward = 0
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, term, trunc, _ = env.step(action)
            agent.memory.push(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            agent.optimize_model()
            if trunc:
                print('agent got trunced')
            done = term or trunc

        agent.epsilon_decay()
        if episode % 100 == 0:
            agent.target_net.load_state_dict(agent.policy_net.state_dict())
        print(f'Episode: {str(episode).zfill(5)}, Epsilon: {agent.epsilon:.3f}, Reward: {total_reward:.2f}')
    torch.save(agent.target_net.state_dict(), 'lunar3.pth')
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

