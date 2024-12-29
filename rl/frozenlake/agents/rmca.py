import numpy as np

# project imports
from rl.frozenlake.agents.base import Agent, Trajectory


class RMCAgent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.returns = np.zeros((env.state_space.n,
                                 env.action_space.n))
        self.counts = np.zeros((env.state_space.n,
                                env.action_space.n))
        self.state_value = np.zeros(env.state_space.n)

    def get_action(self, state):
        return self.env.action_space.sample()

    def generate_trajectory(self):
        trajectory = []
        state, _, _ = self.env.reset()
        done = False
        while not done:
            action = self.get_action(state)
            next_state, reward, term, trunc, info = self.env.step(action)
            ts = Trajectory(state=state, action=int(action), reward=reward)
            trajectory.append(ts)
            if term or trunc:
                done = True
            state = next_state
        return trajectory

    def run_episode(self):
        trajectory = self.generate_trajectory()
        episode_reward = 0
        for i, t in enumerate(reversed(trajectory)):
            state, action, reward = t.state, t.action, t.reward
            episode_reward += reward
            self.returns[state, action] += episode_reward
            self.counts[state, action] += 1

    def update(self):
        tmp = np.divide(self.returns,
                        self.counts,
                        out=np.zeros_like(self.returns),
                        where=self.counts != 0)
        self.state_value = np.max(tmp, axis=1)

