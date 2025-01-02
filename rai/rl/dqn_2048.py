import torch

from rai.rl.envs.g2048 import Game2048
from rai.rl.agents.dqn_2048 import DQLAgent


if __name__ == "__main__":
    env = Game2048()
    agent = DQLAgent()

    episodes = 1000
    for e in range(episodes):
        state = env.reset()
        total_reward = 0
        while True:
            action = agent.act(state)
            next_state, reward, done = env.move(action)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            if done:
                print(f"Episode {e + 1}/{episodes}, Score: {total_reward}")
                break

            agent.replay()
            agent.steps += 1
            if agent.steps % agent.update_target_steps == 0:
                agent.update_target_model()

        agent.decay_epsilon()
    torch.save(agent.model.state_dict(), 'dql_2048.pth')
