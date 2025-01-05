from abc import ABC
from gymnasium.spaces import Discrete

# project imports
from rai.utils.models import Trajectory


class Learner(ABC):
    def __init__(self,
                 obs_space: Discrete,
                 action_space: Discrete,
                 params=None):
        self.obs_space = obs_space
        self.action_space = action_space
        self.params = params
        self.trajectory: Trajectory = Trajectory()

    def reset(self) -> None:
        self.trajectory = Trajectory()

    def policy(self, state: int) -> int:
        raise NotImplementedError

    def process_step(self) -> None:
        raise NotImplementedError

    def process_episode(self, episode: int) -> None:
        raise NotImplementedError

    def learn(self):
        raise NotImplementedError
