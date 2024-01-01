"""
trying to implement different agent types of aima
"""


class Environment:
    pass


class State:
    pass


class Sensor:
    pass


class Percept:
    pass


class Actuator:
    pass


class Action:
    pass


class Rule:
    pass


class ConditionActionRule(Rule):
    pass


class Agent:
    def __init__(self):
        self.sensors = None
        self.actuators = None
        self.rules = None

    def agent_program(self, percept):
        """ returns an action """ 



