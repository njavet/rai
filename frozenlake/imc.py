import numpy as np

# project imports
from frozenlake.helpers import rand_argmax


def choose_random_action(env):
    action = env.action_space.sample()
    return action


def choose_eps_greedy(env, eps, state, qtable):
    if np.random.rand() < eps:
        action = env.action_space.sample()
    else:
        action = rand_argmax(qtable[state])
    return action


def update_qtable(params, qtable, state, action, reward, new_state):
    """ Q-function update
            Q_update(s,a):= Q(s,a) + learning_rate * delta
                delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """
    # Compute the temporal difference (TD) target
    bfq = params.gamma * rand_argmax(qtable[new_state])
    delta = reward + bfq - qtable[state, action]
    qtable[state, action] = (qtable[state, action] + params.alpha * delta)
