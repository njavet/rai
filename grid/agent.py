from pydantic import BaseModel
import numpy as np
from collections import defaultdict

# project imports
from grid.environment import Action, State


class Trajectory(BaseModel):
    state: State
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
        self.qtable = np.zeros((self.env.height, self.env.width, len(self.action_space)), dtype=np.float64)
        self.counts = np.zeros((self.env.height, self.env.width, len(self.action_space)), dtype=np.int8)
        self.action_to_int = {Action.LEFT: 0,
                              Action.DOWN: 1,
                              Action.RIGHT: 2,
                              Action.UP: 3}

    def choose_action(self):
        ind = np.random.randint(0, len(self.action_space))
        return self.action_space[ind]

    def generate_trajectory(self):
        trajectory = []
        n_steps = 0
        state, _, _ = self.env.reset()
        print('state', state.x, state.y)
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
            x, y = state.x, state.y
            if x == 0 and y == 0:
                print('yo, rewards', reward, episode_reward)
            a = self.action_to_int[action]
            self.qtable[x, y, a] += episode_reward
            self.counts[x, y, a] += 1

    def action_value(self, x, y, action):
        try:
            val = self.qtable[x, y, action] / self.counts[x, y, action]
        except ZeroDivisionError:
            val = 0.
        return val
