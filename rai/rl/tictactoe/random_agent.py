from collections import defaultdict
import json
import random


class Agent:
    def __init__(self,
                 init_state,
                 exploration_rate=0.1,
                 step_size=0.1,
                 sym='X') -> None:
        self.exploration_rate = exploration_rate
        self.step_size = step_size
        self.sym = sym
        self.model = self._load_model('model.json')
        self.state = init_state
        self.action = Action(self.state, self.exploration_rate)

    @staticmethod
    def _load_model(file_name):
        try:
            with open(file_name) as f:
                model = json.load(f)
        except FileNotFoundError:
            model = defaultdict(float)
        return model

    @staticmethod
    def _save_model(model, file_name):
        with open(file_name, 'w') as f:
            json.dump(model, f, indent=2)

    def act(self):
        return self.action.get_action()


class Action:
    def __init__(self, state, exploration_rate):
        self.state = state
        self.exploration_rate = exploration_rate

    def get_action(self):
        if self.state.is_init():
            return self._opening_action()

        free_cells = self.state.get_free_cells()
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(free_cells)

        for cell in free_cells:



    @staticmethod
    def _opening_action():
        """ three equivalent actions:
        corner, edge, center """
        opening = random.random()
        # corner
        if opening < 0.33:
            # 4 equivalent corners
            corner = random.random()
            if corner < 0.25:
                return 0
            elif corner < 0.5:
                return 2
            elif corner < 0.75:
                return 6
            else:
                return 8
        # edge
        if 0.33 <= opening < 0.66:
            # 4 equivalent edges
            edge = random.random()
            if edge < 0.25:
                return 1
            elif edge < 0.5:
                return 3
            elif edge < 0.75:
                return 5
            else:
                return 7
        # center
        else:
            return 4
