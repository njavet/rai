import numpy as np
from selenium.webdriver.common.by import By
import time

# project imports
from rai.g2048.ffctrl import FirefoxControl
from rai.g2048.agent import find_best_move


def play_2048():
    fc = FirefoxControl()
    try:
        fc.driver.get(fc.url)
        fc.game_container = fc.driver.find_element(By.TAG_NAME, 'body')
        fc.game_container.click()
        fc.game_message = fc.driver.find_element(By.CLASS_NAME, 'game-message')
        fc.score_element = fc.driver.find_element(By.CLASS_NAME, 'score-container')

        while True:
            board = fc.get_board()
            grid = np.array(board)
            move = find_best_move(grid)
            fc.send_move(move)
            score = fc.get_score()
            print('SCORE', score)
            status = fc.get_status()
            if 'game over' in status.lower():
                break
            time.sleep(0.1)

        print('final board:')
        for row in board:
            print(row)
        print('final score:', score)
        time.sleep(5)
    finally:
        fc.driver.quit()
