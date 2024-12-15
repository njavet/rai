from grid.environment import Action, State, Reward


class Agent:
    def __init__(self):
        self.state = None
        self.reward = None

    def policy(self, state: State) -> Action:
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



