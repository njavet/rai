import numpy as np

# project imports
from rl.frozenlake.agents.base import Agent


class QAgent(Agent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.qtable = np.zeros((params.state_size, params.action_size))

    def get_action(self, state, learning):
        if np.random.rand() < self.params.epsilon and learning:
            action = self.env.action_space.sample()
        else:
            action = self.random_argmax(self.qtable[state])
        return action

    def update_qtable(self, state, action, reward, next_state):
        """ Q-function update
             Q_update(s,a):= Q(s,a) + learning_rate * delta
                 delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """
        # Compute the temporal difference (TD) target
        bfq = self.params.gamma * np.argmax(self.qtable[next_state])
        delta = self.params.alpha * (reward + bfq - self.qtable[state, action])
        self.qtable[state, action] = self.qtable[state, action] + delta

    def run_episode(self, learning=True):
        trajectory = self.generate_trajectory(learning)
