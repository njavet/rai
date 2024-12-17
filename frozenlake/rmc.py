from collections import defaultdict


def run(env, params):
    trajectories = []
    values = defaultdict(float)
    counts = defaultdict(float)
    action_value = defaultdict(float)

    for episode in range(params.total_episodes):
        trajectory = []
        done = False
        state, info = env.reset()
        while not done:
            action = env.action_space.sample()
            next_state, reward, term, trunc, info = env.step(action)
            trajectory.append((state, reward, action))
            state = next_state
            if trunc:
                print('trunc', next_state, reward, action)
            elif term:
                print('term', next_state, reward, action)
            done = term or trunc

        trajectories.append(trajectory)
    return trajectories
