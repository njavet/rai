import unittest


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board0 = 'XO OX O X'
        self.board1 = 'XOXO  XXX'

    def test_winning_row(self):
        pass


if __name__ == '__main__':
    unittest.main()

