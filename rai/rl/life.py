
# project imports
from rai.utils.models import Trajectory, TrajectoryStep


class Life:
    def __init__(self, env, params):
        """ params could be seen as given by nature / god """
        self.env = env
        self.params = params
        self.trajectory = Trajectory()

    # TODO policy should be from the agent
    #  problem it an agent should have learners, but therefore they
    #  should not inherit from the agent class itself
    def policy(self, state: int) -> int:
        raise NotImplementedError

    def reset(self):
        self.trajectory = Trajectory()

    def exec_step(self, state: int, action: int) -> tuple[int, TrajectoryStep, bool]:
        next_state, reward, term, trunc, info = self.env.step(action)
        ts = TrajectoryStep(state=state, action=int(action), reward=reward)
        done = term or trunc
        return next_state, ts, done

    def process_step(self, next_state):
        pass

    def generate_trajectory(self):
        # self reset
        self.reset()
        state, info = self.env.reset()
        done = False
        while not done:
            action = self.policy(state)
            next_state, ts, done = self.exec_step(state, action)
            self.trajectory.steps.append(ts)
            # the agent might want to do something after each step
            self.process_step(next_state)
            state = next_state

    def process_episode(self, episode):
        pass
