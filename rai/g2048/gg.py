import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()


try:
    driver.get('https://2048game.com')
    game_container = driver.find_element(By.TAG_NAME, 'body')
    game_message = driver.find_element(By.CLASS_NAME, 'game-message')
    score_element = driver.find_element(By.CLASS_NAME, 'score-container')
    moves = [Keys.ARROW_UP, Keys.ARROW_RIGHT, Keys.ARROW_DOWN, Keys.ARROW_LEFT]


    # Automate gameplay by sending arrow key inputs
    for _ in range(200):  # Play for 100 moves (adjust as needed)
        for move in moves:
            game_container.send_keys(move)
            board = [[0 for _ in range(4)] for _ in range(4)]
            tile_container = driver.find_element(By.CLASS_NAME, "tile-container")
            tiles = tile_container.find_elements(By.CLASS_NAME, "tile")
            for tile in tiles:
                tile_classes = tile.get_attribute("class").split()
                value = int([cls.split("-")[1] for cls in tile_classes if cls.startswith("tile-") and cls[5].isdigit()][0])
                position_class = [cls for cls in tile_classes if cls.startswith("tile-position-")][0]
                print('pos', position_class)
                _, _, x, y = position_class.split("-")
                x, y = int(x) - 1, int(y) - 1  # Convert to zero-based index
                print('x', x, 'y', y)
                board[y][x] = value

            for row in board:
                print(row)
            print('score:', score_element.text.split()[0])
            print('gamemsg:', game_message.text)
            time.sleep(5)  # Small d


finally:
    driver.quit()

