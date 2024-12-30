import numpy as np
from collections import defaultdict

# project imports
from rai.agents.base import SchopenhauerAgent
from rai.utils.helpers import random_argmax
from rai.utils.models import Params, TrajectoryStep, Trajectory


class RLAgent(SchopenhauerAgent):
    def __init__(self, env, params: Params):
        super().__init__(env, params)
        self.vtable = np.zeros(params.state_size)
        self.qtable = np.zeros((params.state_size, params.action_size))
        self.trajectories = defaultdict(list)

    def get_action(self, state: int) -> int:
        action = random_argmax(self.qtable[state])
        return action

    def exec_step(self, state: int, action: int) -> tuple[int, TrajectoryStep, bool]:
        next_state, reward, term, trunc, info = self.env.step(action)
        ts = TrajectoryStep(state=state, action=int(action), reward=reward)
        done = term or trunc
        return next_state, ts, done

    def process_step(self, *args):
        pass

    def process_episode(self, *args):
        pass

    def generate_trajectory(self) -> Trajectory:
        trajectory = Trajectory(steps=[])
        state, info = self.env.reset()
        done = False
        while not done:
            action = self.get_action(state)
            next_state, ts, done = self.exec_step(state, action)
            state = next_state
            trajectory.steps.append(ts)
            self.process_step()
        return trajectory

    def evaluate_trajectory(self, trajectory: Trajectory) -> tuple[np.ndarray, np.ndarray]:
        returns = np.zeros((self.params.state_size, self.params.action_size))
        counts = np.zeros((self.params.state_size, self.params.action_size))
        total_reward = 0
        for t in reversed(trajectory.steps):
            state, action, reward = t.state, t.action, t.reward
            total_reward += reward
            returns[state, action] += total_reward
            counts[state, action] += 1
        return returns, counts

    def evaluate_trajectories(self, trajectories: list[Trajectory]):
        returns = np.zeros((self.params.state_size, self.params.action_size))
        counts = np.zeros((self.params.state_size, self.params.action_size))
        for trajectory in trajectories:
            r, c = self.evaluate_trajectory(trajectory)
            returns += r
            counts += c
        return returns, counts


class Learner(RLAgent):
    def __init__(self, env, params):
        super().__init__(env, params)

    def get_action(self, state: int) -> int:
        raise NotImplementedError

    def reset_q_table(self):
        self.qtable = np.zeros((self.params.state_size, self.params.action_size))

    def update_qtable(self, *args):
        pass

    def run_env(self):
        qtables = np.zeros((self.params.n_runs,
                            self.params.state_size,
                            self.params.action_size))
        for n in range(self.params.n_runs):
            self.reset_q_table()
            for episode in range(self.params.total_episodes):
                trajectory = self.generate_trajectory()
                self.trajectories[episode].append(trajectory)
            self.process_episode()
            qtables[n, :, :] = self.qtable
        self.qtable = qtables.mean(axis=0)


class RMCLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)

    def get_action(self, state):
        action = self.env.action_space.sample()
        return action

    def process_episode(self, *args):
        returns, counts = self.evaluate_trajectories(self.trajectories.values())
        self.update_qtable(returns, counts)

    def update_qtable(self, returns, counts):
        self.qtable = np.divide(returns,
                                counts,
                                out=np.zeros_like(returns),
                                where=counts != 0)


class IMCAgent(Agent):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.returns = np.zeros((params.state_size, params.action_size))
        self.counts = np.zeros((params.state_size, params.action_size))

    def get_action(self, state):
        if np.random.rand() < self.params.epsilon:
            action = self.env.action_space.sample()
        else:
            action = self.get_optimal_action(state)
        return action

    def run_episode(self):
        trajectory = self.generate_trajectory(self.get_action)
        episode_reward = 0
        for i, t in enumerate(reversed(trajectory)):
            state, action, reward = t.state, t.action, t.reward
            episode_reward += reward
            self.returns[state, action] += episode_reward
            self.counts[state, action] += 1
        self.update()

    def update(self):
        self.qtable = np.divide(self.returns,
                                self.counts,
                                out=np.zeros_like(self.returns),
                                where=self.counts != 0)
        self.vtable = np.max(self.qtable, axis=1)


class QLearner(Learner):
    def __init__(self, env, params):
        super().__init__(env, params)

    def get_action(self, state):
        if np.random.rand() < self.params.epsilon:
            action = self.env.action_space.sample()
        else:
            action = random_argmax(self.qtable[state])
        return action

    def process_step(self, state, action, reward, next_state):
        """ Q-function update
             Q_update(s,a):= Q(s,a) + learning_rate * delta
                 delta =  [R(s,a) + gamma * max Q(s',a') - Q(s,a)] """
        # Compute the temporal difference (TD) target
        bfq = self.params.gamma * np.argmax(self.qtable[next_state])
        delta = self.params.alpha * (reward + bfq - self.qtable[state, action])
        self.qtable[state, action] = self.qtable[state, action] + delta
