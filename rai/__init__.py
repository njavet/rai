from .rl.envs.grid import GridEnv
from gymnasium.envs.registration import register

register(
    id='rai/rai/rl/envs/Game2048-v0',
    entry_point='rai:GridEnv',
)

