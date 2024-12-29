from pydantic import BaseModel
import numpy as np

# project imports
from grid.environment import Action


class Trajectory(BaseModel):
    state: tuple[int, int]
    action: Action
    reward: float


class Agent:
    def __init__(self, env, max_steps: int = 1024, debug: bool = False):
        # This would be a schopenhauer agent, since the "world" is part
        # of the agent, not the other way round
        self.env = env
        self.max_steps = max_steps
        self.debug = debug
        self.action_space = [action for action in Action]
        self.qtable = np.zeros((self.env.height, self.env.width, len(self.action_space)),
                               dtype=np.float64)
        self.counts = np.zeros((self.env.height, self.env.width, len(self.action_space)),
                               dtype=np.float64)

    def choose_action(self):
        ind = np.random.randint(0, len(self.action_space))
        return self.action_space[ind]

    def generate_trajectory(self):
        trajectory = []
        n_steps = 0
        state, _, _ = self.env.reset()
        terminal = False
        while not terminal:
            action = self.choose_action()
            next_state, reward, terminal = self.env.step(action)
            t = Trajectory(state=state, action=action, reward=reward)
            trajectory.append(t)
            n_steps += 1
            state = next_state

            if n_steps > self.max_steps:
                print('abort due to too many steps...')
                terminal = True
        return trajectory

    def run_episode(self):
        trajectory = self.generate_trajectory()
        episode_reward = 0
        for i, t in enumerate(reversed(trajectory)):
            state, action, reward = t.state, t.action, t.reward
            episode_reward += reward
            x, y = state
            self.qtable[x, y, action.value] += episode_reward
            self.counts[x, y, action.value] += 1

    def action_value(self, x, y, action):
        div = self.counts[x, y, action]
        if div == 0:
            return 0.0
        return self.qtable[x, y, action] / div

    def policy(self, state):
        x, y = state
        ind = np.argmax([self.action_value(x, y, a.value) for a in self.action_space])
        return self.action_space[ind]

    def run(self):
        trajectory = []
        n_steps = 0
        state, _, _ = self.env.reset()
        terminal = False
        while not terminal:
            action = self.policy(state)
            next_state, reward, terminal = self.env.step(action)
            t = Trajectory(state=state, action=action, reward=reward)
            trajectory.append(t)
            n_steps += 1
            state = next_state
        return trajectory


