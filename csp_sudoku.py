
"""
a constraint satisfaction problem consists of three components:
    X: set of variables
    D:  set of domains, one for each variable
    C: constraints that specify allowable combinations of values

"""
import itertools
import collections


grid = [0, 0, 0, 0, 0, 6, 0, 7, 0,
        8, 0, 1, 4, 7, 3, 0, 0, 0,
        7, 0, 0, 0, 0, 1, 9, 0, 0,
        6, 0, 0, 0, 0, 0, 0, 0, 9,
        0, 5, 0, 0, 0, 0, 0, 0, 0,
        9, 0, 0, 5, 0, 8, 0, 0, 4,
        4, 0, 0, 0, 0, 0, 0, 0, 1,
        1, 6, 2, 0, 3, 0, 0, 0, 0,
        0, 0, 0, 2, 0, 0, 4, 0, 0]


class Agent:
    def __init__(self, grid):
        self.state = self._preprocess_input(grid)
        self.variables = self._get_variables()

    @staticmethod
    def _preprocess_input(grid):
        return grid

    def _get_variables(self):
        return [ind for ind, val in enumerate(self.state) if val == 0]
    
    def _get_row(self, ind):
        pass
    def _get_col(self, ind):
        pass
    def _get_box(self, ind):
        pass

