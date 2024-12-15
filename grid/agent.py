from collections import defaultdict

# project imports
from grid.environment import Action, State, Reward


class Agent:
    def __init__(self):
        self.state_t = 3, 0
        self.reward_t = 0
        self.policy = [[2, 2, 2, 2, 3],
                       [1, 0, 2, 2, 3],
                       [1, 0, 1, 0, 0],
                       [0, 2, 2, 2, 1],
                       [2, 2, 2, 2, 1]]
        self.value = [[-6, -5, -4, -3, -2],
                      [-7, 0, -3, -2, -1],
                      [-8, 0, -4, 0, 0],
                      [0, -4, -3, -2, -1],
                      [-6, -5, -4, -3, -2]]
        self.reward = [[-1, -1, -1, -1, -1],
                       [-1, 0, -1, -1, -1],
                       [-1, 0, -1, 0, -1],
                       [0, -1, -1, -1, -1],
                       [-1, -1, -1, -1, -1]]

    def _policy(self, state: State) -> Action:
        """
        the policy p(a|s) = P[At = a | St = s]
        maps an action At to a given state St where At has probability P

        """
        pass

    def value_function(self, state: State) -> float:
        """
        The value function computes the expectation value given a policy
        of the total reward in this state: V = E[sum(rewards) | St = s]

        """
        pass

    def predict_next_state(self, state: State, action: Action) -> State:
        pass

    def predict_next_reward(self, state: State, action: Action) -> Reward:
        pass



