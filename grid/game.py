
from grid.agent import Agent


def main():
    state_0 = 3, 0
    reward_0 = 0
    agent = Agent(state_0, reward_0)

    while not agent.terminal_state():
        x, y = agent.state_t
        action = agent.policy[x][y]
        if action == 1:
            agent.state_t = agent.state_t[0] - 1, agent.state_t[1]
        elif action == 2:
            agent.state_t = agent.state_t[0], agent.state_t[1] + 1
        elif action == 3:
            agent.state_t = agent.state_t[0] + 1, agent.state_t[1]
        elif action == 4:
            agent.state_t = agent.state_t[0], agent.state_t[1] - 1
        print(agent.state_t)
        agent.reward_t = -1
        agent.total += agent.reward_t

    print('agent in position', agent.state_t)
    print('agent value:', agent.total)
