from abc import ABC

# project imports
from rai.rl.life import Life


class SchopenhauerAgent(ABC):
    """
    For now lets define a SchopenhauerAgent as an Agent
    that has an environment as part of himself. So the environment exists
    only inside the agent. Another type would be a Cartesian Agent that is
    part of the environment. The third Agent type would be a mix of both.
    """
    def __init__(self, env, params):
        """ params could be seen as given by nature / god """
        self.env = env
        self.params = params
        self.life = Life(env, params)

