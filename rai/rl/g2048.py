from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# project imports
from rai.g2048.ffctrl import FirefoxControl
from rai.g2048.agent import Agent


class G2048:
    def __init__(self, url='https://2048game.com'):
        self.url = url
        self.driver = webdriver.Firefox()
        self.game_container = None
        self.game_message = None
        self.score_element = None
        self.agent = Agent()
        self.moves = {0: Keys.ARROW_LEFT,
                      1: Keys.ARROW_DOWN,
                      2: Keys.ARROW_RIGHT,
                      3: Keys.ARROW_UP}

    def get_board(self):
        board = [[0 for _ in range(4)] for _ in range(4)]
        tile_container = self.driver.find_element(By.CLASS_NAME,
                                                  'tile-container')
        tiles = tile_container.find_elements(By.CLASS_NAME, 'tile')
        for tile in tiles:
            tile_classes = tile.get_attribute('class').split()
            value = int([cls.split('-')[1] for cls in tile_classes if
                         cls.startswith('tile-') and cls[5].isdigit()][0])
            position_class = [cls for cls in tile_classes if
                              cls.startswith('tile-position-')][0]
            _, _, x, y = position_class.split('-')
            x, y = int(x) - 1, int(y) - 1
            board[y][x] = value
        return board

    def get_score(self):
        return int(self.score_element.text.split()[0])

    def get_status(self):
        return self.game_message.text

    def send_move(self, move):
        key = self.moves[move]
        self.game_container.send_keys(key)

    def play(self):
        try:
            self.driver.get(self.url)
            self.game_container = self.driver.find_element(By.TAG_NAME, 'body')
            self.game_container.click()
            self.game_message = self.driver.find_element(By.CLASS_NAME, 'game-message')
            self.score_element = self.driver.find_element(By.CLASS_NAME, 'score-container')

            while True:
                board = self.get_board()
                move = self.agent.find_best_move(board)
                self.send_move(move)
                score = self.get_score()
                print('SCORE', score)
                status = self.get_status()
                if 'game over' in status.lower():
                    break
                time.sleep(0.1)

            print('final board:')
            for row in board:
                print(row)
            print('final score:', score)
            time.sleep(5)
        finally:
            self.driver.quit()


def play_2048():
    game = G2048()
    game.play()
