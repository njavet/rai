import numpy as np
import random


class Game2048:
    def __init__(self):
        self.board = np.zeros((4, 4), dtype=int)
        self.reset()

    def reset(self):
        self.board = np.zeros((4, 4), dtype=int)
        self.add_random_tile()
        self.add_random_tile()
        return self.get_state()

    def add_random_tile(self):
        empty_tiles = [(r, c) for r in range(4) for c in range(4) if self.board[r, c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.board[r, c] = 2 if random.random() < 0.9 else 4

    def get_state(self):
        one_hot = np.zeros((4, 4, 16))
        for r in range(4):
            for c in range(4):
                if self.board[r, c] > 0:
                    one_hot[r, c, int(np.log2(self.board[r, c]))] = 1
        return one_hot.flatten()

    def move(self, action):
        # Action: 0=Up, 1=Down, 2=Left, 3=Right
        if action == 0:
            moved, score = self.merge()
        elif action == 1:
            self.board = np.rot90(self.board, 1)
            moved, score = self.merge()
            self.board = np.rot90(self.board, -1)
        elif action == 2:
            self.board = np.fliplr(self.board)
            moved, score = self.merge()
            self.board = np.fliplr(self.board)
        elif action == 3:
            self.board = np.rot90(self.board, -1)
            moved, score = self.merge()
            self.board = np.rot90(self.board, 1)
        if moved:
            self.add_random_tile()
        return self.get_state(), score, not self.can_move()

    def merge(self):
        moved = False
        score = 0
        new_board = np.zeros_like(self.board)
        for r in range(4):
            tiles = self.board[r, self.board[r] > 0]
            merged = []
            skip = False
            for i in range(len(tiles)):
                if skip:
                    skip = False
                    continue
                if i < len(tiles) - 1 and tiles[i] == tiles[i + 1]:
                    merged.append(tiles[i] * 2)
                    score += tiles[i] * 2
                    skip = True
                else:
                    merged.append(tiles[i])
            new_board[r, :len(merged)] = merged
            if not np.array_equal(new_board[r], self.board[r]):
                moved = True
        self.board = new_board
        return moved, score

    def can_move(self):
        if np.any(self.board == 0):
            return True
        for r in range(4):
            for c in range(4):
                if (r > 0 and self.board[r, c] == self.board[r - 1, c]) or \
                   (c > 0 and self.board[r, c] == self.board[r, c - 1]):
                    return True
        return False
