from collections import defaultdict
import collections
import json
import random
import json
import random

# project imports
from rai.rl.life import Life


class Agent(Life):
    def __init__(self, env, params):
        super().__init__(env, params)
        self.model = self._load_model('model.json')

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

    def policy(self, state: int) -> int:
        

    def get_best_action(board, model, turn, debug=False):
        free_fields = engine.get_free_fields(board)

        if board == engine.get_initial_board():
            return _opening_action()

        if random.uniform(0, 1) < exploration_rate:
            print('explore')
            return random.choice(free_fields)

        best_prob = 0
        chosen_field = free_fields[0]
        for ind, field in enumerate(free_fields):

            new_board = engine.insert_symbol(board, turn, field)
            win_prob = model.get(new_board, 0.5)

            if best_prob < win_prob:
                best_prob = win_prob
                chosen_field = field
            if debug:
                print('field', field, 'winprob', win_prob)
        return chosen_field

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



def train_model(number_of_games, model_file_name):
    model = {}
    winners = collections.defaultdict(int)
    for game_nr in range(number_of_games):
        who_won = _play_game(model)
        winners[who_won] += 1
    _save_model(model, model_file_name)

    for k, v in winners.items():
        print(k, v)


def _play_game(model):
    board = engine.get_initial_board()
    while True:
        turn = engine.whos_turn(board)
        if turn == 'X':
            field = get_best_action(board, model, turn)
            old_board = board
            board = engine.make_move(board, field, turn)
            _update_model(old_board, board, step_size, model)
            assert(board != '')
        else:
            field = _get_opponent_action(board)
            board = engine.make_move(board, field, turn)

        game_over, who_won, reward = engine.evaluate(board)
        if game_over:
            _learn_from_final_move(board, model, who_won)
            return who_won
