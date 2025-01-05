from .rl.envs.grid import GridEnv
from gymnasium.envs.registration import register

register(
    id='rai/GridEnv-v0',
    entry_point='rai:GridEnv',
)

