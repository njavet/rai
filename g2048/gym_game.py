from rich.text import Text
from rich.console import Console

import copy
import random
import math
import collections
import functools
import itertools

import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces


class Env2048(gym.Env):
    metadata = {'render_modes': ['human', 'rgb_array'], 'render_fps': 4}

    def __init__(self, render_mode=None, size=4):
        self.size = size
        self.window_size = 512
        self.observation_space = spaces.Box(
            0, 2**16, shape=(4, 4), dtype=np.int16
        )
        # up - 0, down - 1, left - 2, right -3
        self.action_space = spaces.Discrete(4)
        self._action_to_direction = {
            0: None
        }

        assert render_mode is None or render_mode in self.metadata
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        info = {}
        observation = np.zeros((4, 4))
        observation = self.add_random_tile(observation)
        observation = self.add_random_tile(observation)
        return observation, info

    def step(self, action):
        pass
