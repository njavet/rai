from typing import Any
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import pygame
from gymnasium.core import RenderFrame, ObsType


# project imports


class GridEnv(gym.Env):
    def __init__(self, m: int = 4, n: int = 4, max_steps: int = 300, render_mode=None):
        super().__init__(render_mode)
        self.m = m
        self.n = n
        self.agent_pos = 0
        self.term = m * n - 1
        self.steps = 0
        self.max_steps = max_steps

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        self.steps = 0
        self.agent_pos = 0
        return self.agent_pos, {'start': 0}

    def pos_to_tuple(self):
        """ convert integer position to grid position"""
        x, y = divmod(self.agent_pos, self.m)
        return x, y

    def update_agent_position(self, ax, ay):
        x, y = self.pos_to_tuple()
        x1 = max(x + ax, 0)
        y1 = max(y + ay, 0)
        x_new = min(x1, self.m - 1)
        y_new = min(y1, self.n - 1)
        self.agent_pos = x_new * self.m + y_new

    @staticmethod
    def get_action_values(action):
        if action.value == 0:
            return 0, -1
        elif action.value == 1:
            return 1, 0
        elif action.value == 2:
            return 0, 1
        elif action.value == 3:
            return -1, 0
        raise ValueError('invalid action')

    def step(self, action):
        self.steps += 1
        ax, ay = self.get_action_values(action)
        self.update_agent_position(ax, ay)
        reward = -1
        is_terminal = self.agent_pos == self.term
        trunc = self.steps >= self.max_steps
        return self.agent_pos, reward, is_terminal, trunc, None
