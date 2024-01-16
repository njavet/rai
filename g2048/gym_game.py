from rich.text import Text
import json
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
import utils2048


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

        assert render_mode is None or render_mode in self.metadata
        self.render_mode = render_mode

        self.window = None
        self.clock = None

        # to have the 'observation' in the step function,
        # probably n00b style
        self.state = None
        self.score = 0
        self.steps = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        info = {}
        observation = np.zeros((4, 4), dtype=np.int16)
        observation = utils2048.add_random_tile(observation)
        observation = utils2048.add_random_tile(observation)
        self.state = observation
        self.score = 0
        self.steps = 0
        return observation, info

    def step(self, action):
        self.steps += 1
        if not utils2048.is_move_available(self.state, action):
            return self.state, -2048, False, False, None

        if action == 0:
            observation, reward = utils2048.merge_up(self.state)
        elif action == 1:
            observation, reward = utils2048.merge_down(self.state)
        elif action == 2:
            observation, reward = utils2048.merge_left(self.state)
        elif action == 3:
            observation, reward = utils2048.merge_right(self.state)

        observation = utils2048.add_random_tile(observation)
        if observation is None:
            terminated = True
        elif not utils2048.available_moves(observation):
            terminated = True
        else:
            terminated = False
            self.state = observation
        self.score += reward
        return observation, reward, terminated, False, None

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


def baseline_random_moves(fname=None):
    env = Env2048()
    observation, info = env.reset()
    random_games = []

    for _ in range(1000):
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            random_games.append({'score': env.score,
                                 'max_tile': env.state.max(),
                                 'steps': env.steps})
            observation, info = env.reset()
    env.close()

    if fname:
        with open(fname, 'a') as f:
            json.dump(random_games, f, indent=2)
    else:
        return random_games


def utility(grid):
    """
        the goal is to find the correct weights to combine the obviously
        good heuristics:
        zeros: number of empty cells, the more, the better
        rank: maximum tile, the higher, the better
        edge / corner: large tiles in corner or at the edges
        monotony: a monotonously decreasing / increasing board is easier to merge
        adjacency: the more tiles with the same value are close together, the better
        how important are the values of the tiles in the mono / adj, edge score ?

        return bias +
               w0 * zeros +
               w1 * rank +
               w2 * edge +
               w3 * mono +
               w4 * adj
    :param grid: 2d numpy array shape (4, 4)
    :return: computed score of this state
    """
    zeros = grid.size - np.count_nonzero(grid)
    rank = grid.max()

    score = 0
    for row in node.grid:
        score += score_seq(tuple(row))
    for col in zip(*node.grid):
        score += score_seq(tuple(col))
    #print('score:', score)
    return score


def score_seq(seq):
    # large tiles on the edge
    ind = seq.index(rank)
    if ind == 0 or ind == 3:
        edge = 1 - rw
    else:
        edge = 0

    # monotonous
    mono = 0
    mon_inc = all([val <= seq[i + 1] for i, val in enumerate(seq[:-1])])
    mon_dec = all([seq[i + 1] <= val for i, val in enumerate(seq[:-1])])
    if mon_inc:
        mono += 2
    if mon_dec:
        mono += 2

    adj = 0
    for i, val in enumerate(seq[1:]):
        if val == seq[i + 1]:
            adj += 1 - rw

    return zeros + edge + mono + adj

