import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class FirefoxControl:
    def __init__(self, url='https://2048game.com'):
        self.url = url
        self.driver = webdriver.Firefox()
        self.game_container = None
        self.game_message = None
        self.score_element = None

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

    def get_game_message(self):
        return self.game_message.text

    def send_move(self, move):
        self.game_container.send_keys(move)

    def start_game(self):
        try:
            self.driver.get(self.url)
            self.game_container = self.driver.find_element(By.TAG_NAME,
                                                           'body')
            self.game_message = self.driver.find_element(By.CLASS_NAME,
                                                         'game-message')
            self.score_element = self.driver.find_element(By.CLASS_NAME,
                                                          'score-container')

            while True:
                time.sleep(0.1)

        finally:
            self.driver.quit()
