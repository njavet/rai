import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import socket


class FirefoxRemoteControl:
    """ Interact with a web browser running the Remote Control extension. """
    def __init__(self, port):
        self.sock = socket.socket()
        self.sock.connect(('localhost', port))

    def execute(self, cmd):
        msg = cmd.replace('\n', ' ') + '\r\n'
        self.sock.send(msg.encode('utf8'))
        ret = []
        while True:
            chunk = self.sock.recv(4096)
            ret.append(chunk)
            if b'\n' in chunk:
                break
        res = json.loads(b''.join(ret).decode('utf8'))
        if 'error' in res:
            raise Exception(res['error'])
        elif not res:
            return None
        else:
            return res['result']


class FRC:
    def __init__(self):
        # Set up the Firefox driver
        self.options = webdriver.FirefoxOptions()
        #self.options.add_argument('--headless')  # Run without a GUI
        self.driver = webdriver.Firefox(options=self.options)

        try:
            # Open the 2048 game
            self.driver.get("https://play2048.co/")

            # Locate the game container
            game_container = self.driver.find_element(By.TAG_NAME, "body")

            # Define a sequence of moves
            moves = [Keys.ARROW_UP, Keys.ARROW_RIGHT, Keys.ARROW_DOWN, Keys.ARROW_LEFT]

            # Play the game automatically
            for _ in range(100):  # Adjust the number of moves
                for move in moves:
                    game_container.send_keys(move)
                    time.sleep(0.1)  # Small delay between moves

            # Optionally: Take a screenshot of the game state
            self.driver.save_screenshot("2048_game_result.png")

        finally:
            # Close the browser
            self.driver.quit()
