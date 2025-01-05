import gymnasium as gym

# project imports
from rai.rl.agents.lunar import Agent


def train_agent():
    env = gym.make('LunarLander-v3',
                   continous=False,
                   gravity=10)

    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    agent = Agent(state_dim,
                  action_dim,
                  lr=0.001,
                  capacity=10000,
                  batch_size=64)
    for episode in range(500):
        state = env.reset()[0]
        total_reward = 0
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, done, _, _ = env.step(action)
            agent.memory.push(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            agent.optimize_model()

        agent.epsilon_decay()
        if episode % 10 == 0:
            agent.target_net.load_state_dict(agent.policy_net.state_dict())
        print(f"Episode: {episode}, Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.2f}")

    return agent


def evaluate():
    agent = train_agent()
    env = gym.make('LunarLander-v3',
                   render_mode='human',
                   continous=False,
                   gravity=10)
    state = env.reset()[0]
    done = False
    total_reward = 0
    while not done:
        action = agent.optimal_policy(state)
        next_state, reward, done, _, _ = env.step(action)
        state = next_state
        total_reward += reward


