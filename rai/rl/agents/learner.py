import numpy as np
from collections import defaultdict

# project imports
from rai.rl.life import Life


class Learner(Life):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.vtable = np.zeros(params.state_size)
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.trajectories = defaultdict(list)

    def reset_q_table(self):
        self.qtable = np.zeros((self.params.state_size, self.params.action_size))

    def process_episode(self, episode) -> tuple[np.ndarray, np.ndarray]:
        returns = np.zeros((self.params.state_size, self.params.action_size))
        counts = np.zeros((self.params.state_size, self.params.action_size))
        total_reward = 0
        for t in reversed(self.trajectory.steps):
            state, action, reward = t.state, t.action, t.reward
            total_reward += reward
            returns[state, action] += total_reward
            counts[state, action] += 1
        return returns, counts

    def process_episodes(self):
        pass

    def run_env(self):
        qtables = np.zeros((self.params.n_runs,
                            self.params.state_size,
                            self.params.action_size))
        for n in range(self.params.n_runs):
            self.reset_q_table()
            for episode in range(self.params.total_episodes):
                self.generate_trajectory()
                self.trajectories[episode].append(self.trajectory)
                # the agent might want to do something after each episode
                self.process_episode(episode)
            # the agent might want to do something after all episodes
            self.process_episodes()
            qtables[n, :, :] = self.qtable
        self.qtable = qtables.mean(axis=0)
