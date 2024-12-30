import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()


try:
    driver.get('https://2048game.com')
    game_container = driver.find_element(By.TAG_NAME, "body")
    game_message = driver.find_element(By.CLASS_NAME, 'game-message')
    score_element = driver.find_element(By.CLASS_NAME, "score-container")
    moves = [Keys.ARROW_UP, Keys.ARROW_RIGHT, Keys.ARROW_DOWN, Keys.ARROW_LEFT]
    # Automate gameplay by sending arrow key inputs
    for _ in range(200):  # Play for 100 moves (adjust as needed)
        for move in moves:
            game_container.send_keys(move)
            time.sleep(0.1)  # Small d
            print('score:', score_element.text.split()[0])
            print('gamemsg:', game_message.text)

    while True:
        # Get user input for direction
        move = input("Enter move (w/a/s/d for UP/LEFT/DOWN/RIGHT, q to quit): ").strip().lower()

        # Map the input to arrow keys
        if move == 'w':
            game_container.send_keys(Keys.ARROW_UP)
        elif move == 's':
            game_container.send_keys(Keys.ARROW_DOWN)
        elif move == 'a':
            game_container.send_keys(Keys.ARROW_LEFT)
        elif move == 'd':
            game_container.send_keys(Keys.ARROW_RIGHT)
        elif move == 'q':
            print("Exiting the game.")
            break
        else:
            print("Invalid input. Use 'w', 'a', 's', 'd', or 'q'.")

finally:
    driver.quit()

