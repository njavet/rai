from pydantic import BaseModel
import numpy as np

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

