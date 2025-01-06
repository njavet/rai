""" agent for basic gym envs, integer states """
from abc import ABC
from pydantic import BaseModel, Field
import gymnasium as gym


class TrajectoryStep(BaseModel):
    state: int
    action: int
    reward: float
    next_state: int
    terminal: bool


class Trajectory(BaseModel):
    steps: list[TrajectoryStep] = Field(default_factory=list)


class SchopenhauerAgent(ABC):
    """
    For now lets define a SchopenhauerAgent as an Agent
    that has an environment as part of himself. So the environment exists
    only inside the agent. Another type would be a Cartesian Agent that is
    part of the environment. The third Agent type would be a mix of both.
    """
    def __init__(self, env: gym.Env) -> None:
        """ params could be seen as given by nature / god """
        self.env = env
        self.trajectory: Trajectory = Trajectory()

    def policy(self, state: int) -> int:
        raise NotImplementedError

    def reset(self) -> None:
        self.trajectory = Trajectory()

    def exec_step(self, state: int, action: int) -> tuple[TrajectoryStep, bool]:
        next_state, reward, term, trunc, info = self.env.step(action)
        ts = TrajectoryStep(state=state,
                            action=action,
                            reward=reward,
                            next_state=next_state,
                            terminal=term)
        done = term or trunc
        return ts, done

    def process_step(self) -> None:
        pass

    def generate_trajectory(self) -> None:
        self.reset()
        state, info = self.env.reset()
        done = False
        while not done:
            action = self.policy(state)
            ts, done = self.exec_step(state, action)
            self.trajectory.steps.append(ts)
            self.process_step()
            state = ts.next_state

    def process_episode(self, episode: int) -> None:
        pass
