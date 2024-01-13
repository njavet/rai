import collections
import json
import random

import t3_engine as engine

exploration_rate = 0.1
step_size = 0.1


def load_model(file_name):
    with open(file_name, 'r') as f:
        model = json.load(f)
    return model


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


def get_minimax_action(board):
    return engine.minimax_decision(board)


def get_expectimax_action(board):
    return engine.expectimax_decision(board)


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


def _save_model(model, model_file_name):
    with open(model_file_name, 'w') as f:
        json.dump(model, f, indent=2)


def _get_opponent_action(board):
    free_fields = engine.get_free_fields(board)
    return random.choice(free_fields)


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


def _update_model(old_state, new_state, step_size, model):
    model[old_state] = model.get(old_state, 0.5) + step_size * (
            model.get(new_state, 0.5) - model.get(old_state, 0.5))


def _learn_from_final_move(old_state, model, winner):
    if winner == 'O':
        model[old_state] = 0
    if winner == 'X':
        model[old_state] = 1


def compute_probability_from_state(board):
    # rows
    over, winner, value = engine.evaluate(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return 0
    else:
        return 0.5
