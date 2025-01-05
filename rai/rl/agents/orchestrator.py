import gymnasium as gym
import torch

# project imports
from rla2048.schemas import OrchestratorParams, TrajectoryStep
from rla2048.agents.learner import Learner


class Orchestrator:
    def __init__(self,
                 env: gym.Env,
                 agent: Learner,
                 params: OrchestratorParams) -> None:
        self.env = env
        self.agent = agent
        self.params = params

    def run_episode(self, episode: int) -> None:
        self.agent.reset_trajectory()
        state, info = self.env.reset()
        terminated = False
        while not terminated:
            action = self.agent.policy(state)
            next_state, reward, term, trunc, info = self.env.step(action)
            terminated = term or trunc
            ts = TrajectoryStep(state=state,
                                action=action,
                                reward=reward,
                                next_state=next_state,
                                done=torch.tensor(terminated, device='cuda'))
            self.agent.trajectory.steps.append(ts)
            self.agent.process_step()
            state = next_state
        self.agent.process_episode(episode)

    def train_agent(self) -> None:
        for n in range(self.params.n_episodes):
            self.run_episode(n)
