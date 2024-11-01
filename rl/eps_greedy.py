

class EpsilonGreedy:
    def __init__(self, epsilon):
        self.epsilon = epsilon

    def choose_action(self, action_space, state, qtable):
        """TODO: Implement the e-greedy algorithm. i.e.:
            with probability epsilon:
                select an action randomly
            else
                select the action with the highest q-value"""

        # Select a random action
        action = action_space.sample()
        return action
