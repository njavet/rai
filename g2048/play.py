import random
import numpy as np
import game
from game import Game, ACTION_NAMES


# pylint: disable=too-many-arguments,too-few-public-methods
class Experience(object):
    def __init__(self,
                 state,
                 action,
                 reward,
                 next_state,
                 game_over,
                 not_available,
                 next_state_available_actions):
        self.state = state
        self.action = action
        self.reward = reward
        self.next_state = next_state
        self.game_over = game_over
        self.not_available = not_available
        self.next_state_available_actions = next_state_available_actions

    def __str__(self):
        return str((self.state,
                    self.action,
                    self.reward,
                    self.next_state,
                    self.game_over,
                    self.next_state_available_actions))

    def __repr__(self):
        return self.__str__()


def play(strategy, verbose=False, allow_unavailable_action=True):
    """Plays a single game, using a provided strategy.

    Args:
      strategy: A function that takes as argument a state and a list of available
          actions and returns an action from the list.
      allow_unavailable_action: Boolean, whether strategy is passed all actions
          or just the available ones.
      verbose: If true, prints game states, actions and scores.

    Returns:
      score, experiences where score is the final score and experiences is the
          list Experience instances that represent the collected experience.
    """

    g2048 = Game()

    state = g2048.state().copy()
    game_over = g2048.game_over()
    experiences = []

    while not game_over:
        if verbose:
            print("Score:", g2048.score())
            g2048.print_state()

        old_state = state
        actions = range(4) if allow_unavailable_action else g2048.available_actions()
        next_action = strategy(old_state, actions)

        if game.is_move_available(g2048.state, next_action):
            reward = g2048.execute_action(next_action)
            state = g2048.state().copy()
            game_over = g2048.game_over()
            if verbose:
                print("Action:", ACTION_NAMES[next_action])
                print("Reward:", reward)
            experiences.append(Experience(old_state,
                                          next_action,
                                          reward,
                                          state,
                                          game_over,
                                          False,
                                          g2048.available_actions()))
        else:
            experiences.append(Experience(state,
                                          next_action,
                                          0,
                                          state,
                                          False,
                                          True,
                                          g2048.available_actions()))

    if verbose:
        print("Score:", g2048.score())
        g2048.print_state()
        print("Game over.")
    return g2048.score(), experiences


def random_strategy(_, actions):
    """Strategy that always chooses actions at random."""
    return np.random.choice(actions)


def static_preference_strategy(_, actions):
    """Always prefer left over up over right over top."""
    return min(actions)


def highest_reward_strategy(state, actions):
    """Strategy that always chooses the action of highest immediate reward.
      If there are any ties, the strategy prefers left over up over right over down.
    """

    sorted_actions = np.sort(actions)[::-1]
    rewards = [Game(np.copy(state)).execute_action(action) for action in sorted_actions]
    action_index = np.argsort(rewards)[-1]
    return sorted_actions[action_index]


def make_greedy_strategy(get_q_values, verbose=False):

    def greedy_strategy(state, actions):
        q_values = get_q_values(state)
        if verbose:
            print("State:")
            print(state)
            print("Q-Values:")
        for action, q_value, action_name in zip(range(4), q_values, ACTION_NAMES):
            not_available_string = "" if action in actions else "(not available)"
            print("%s:\t%.2f %s" % (action_name, q_value, not_available_string))
        sorted_actions = np.argsort(q_values)
        action = [a for a in sorted_actions if a in actions][-1]
        if verbose:
            print("-->", ACTION_NAMES[action])
        return action

    return greedy_strategy


def make_epsilon_greedy_strategy(get_q_values, epsilon):
    greedy_strategy = make_greedy_strategy(get_q_values)

    def epsilon_greedy_strategy(state, actions):
        do_random_action = np.random.choice([True, False], p=[epsilon, 1 - epsilon])
        if do_random_action:
            return random_strategy(state, actions)
        return greedy_strategy(state, actions)

    return epsilon_greedy_strategy
