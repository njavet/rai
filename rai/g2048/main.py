import numpy as np
from selenium.webdriver.common.by import By
import time

# project imports
from rai.g2048.ffctrl import FirefoxControl


def play_2048():
    fc = FirefoxControl()
    moves = list(range(4))
    try:
        fc.driver.get(fc.url)
        fc.game_container = fc.driver.find_element(By.TAG_NAME, 'body')
        fc.game_container.click()
        fc.game_message = fc.driver.find_element(By.CLASS_NAME, 'game-message')
        fc.score_element = fc.driver.find_element(By.CLASS_NAME, 'score-container')

        while True:
            move = np.random.choice(moves)
            fc.send_move(move)
            score = fc.get_score()
            print('SCORE', score)
            if 'game over' in fc.get_game_message().lower():
                break
            time.sleep(0.2)
        board = fc.get_board()
        print('final board:')
        for row in board:
            print(row)

        print('final score:', score)
        time.sleep(5)
    finally:
        fc.driver.quit()
