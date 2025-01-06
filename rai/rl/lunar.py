import gymnasium as gym
from gymnasium.wrappers import RecordVideo
import torch

# project imports
from rai.rl.agents.lunar import Agent


def train_agent():
    env = gym.make('LunarLander-v3',
                   continuous=False,
                   gravity=-10)

    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    agent = Agent(state_dim,
                  action_dim,
                  lr=0.001,
                  capacity=1000000,
                  batch_size=512)
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

