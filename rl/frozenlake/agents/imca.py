import numpy as np

# project imports
from rl.frozenlake.agents.base import Agent, Trajectory


class IMCAgent(Agent):
    def __init__(self, env):
        super().__init__(env)
        self.reached_goal = 0
        self.returns = np.zeros((env.observation_space.n,
                                 env.action_space.n))
        self.counts = np.zeros((env.observation_space.n,
                                env.action_space.n))
        self.qtable = np.zeros((env.observation_space.n,
                                env.action_space.n))
        self.state_value = np.zeros(env.observation_space.n)

    def get_action(self, state):
        return self.env.action_space.sample()

    def policy(self, state):
        return np.argmax(self.qtable[state])

    def generate_trajectory(self, learn=True):
        trajectory = []
        state, info = self.env.reset()
        done = False
        while not done:
            if learn:
                action = self.get_action(state)
            else:
                action = self.policy(state)
            next_state, reward, term, trunc, info = self.env.step(action)
            if not learn:
                print('state', state, 'action', action, 'next', next_state)
            ts = Trajectory(state=state, action=int(action), reward=reward)
            trajectory.append(ts)
            if term or trunc:
                done = True
            state = next_state
        if state == 15:
            self.reached_goal += 1
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
        self.qtable = np.divide(self.returns,
                                self.counts,
                                out=np.zeros_like(self.returns),
                                where=self.counts != 0)
        self.state_value = np.max(self.qtable, axis=1)
