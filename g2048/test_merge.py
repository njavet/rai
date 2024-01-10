import unittest
import game


class TestMerge(unittest.TestCase):
    def setUp(self):

        self.grid0 = [[2, 2, 2, 2],
                      [4, 4, 0, 0],
                      [2, 4, 8, 16],
                      [2, 0, 2, 4]]

        self.grid1 = [[2, 2, 4, 2],
                      [8, 4, 4, 16],
                      [8, 0, 0, 16],
                      [0, 0, 0, 32]]

    def test_merge_left_grid0(self):
        grid = game.merge_left(self.grid0)

        grid_res = [[4, 4, 0, 0],
                    [8, 0, 0, 0],
                    [2, 4, 8, 16],
                    [4, 4, 0, 0]]

        self.assertEqual(grid, grid_res)


    def test_merge_left_grid1(self):
        grid = game.merge_left(self.grid1)

        grid_res = [[4, 4, 2, 0],
                    [8, 8, 16, 0],
                    [8, 16, 0, 0],
                    [32, 0, 0, 0]]

        self.assertEqual(grid, grid_res)

    def test_merge_right_grid0(self):
        grid = game.merge_right(self.grid0)

        grid_res = [[0, 0, 4, 4],
                    [0, 0, 0, 8],
                    [2, 4, 8, 16],
                    [0, 0, 4, 4]]

        self.assertEqual(grid, grid_res)

    def test_merge_right_grid1(self):
        grid = game.merge_right(self.grid1)

        grid_res = [[0, 4, 4, 2],
                    [0, 8, 8, 16],
                    [0, 0, 8, 16],
                    [0, 0, 0, 32]]

        self.assertEqual(grid, grid_res)

        self.grid1 = [[2, 2, 4, 2],
                      [8, 4, 4, 16],
                      [8, 0, 0, 16],
                      [0, 0, 0, 32]]

    def test_merge_up_grid0(self): 
        grid = game.merge_up(self.grid0)

        grid_res = [[2, 2, 2, 2],
                    [4, 8, 8, 16],
                    [4, 0, 2, 4],
                    [0, 0, 0, 0]]

        self.assertEqual(grid, grid_res)

    def test_merge_up_grid1(self): 
        grid = game.merge_up(self.grid1)

        grid_res = [[2, 2, 8, 2],
                    [16, 4, 0, 32],
                    [0, 0, 0, 32],
                    [0, 0, 0, 0]]

        self.assertEqual(grid, grid_res)

    def test_merge_down_grid0(self):
        grid = game.merge_down(self.grid0)

        grid_res = [[0, 0, 0, 0],
                    [2, 0, 2, 2],
                    [4, 2, 8, 16],
                    [4, 8, 2, 4]]

        self.assertEqual(grid, grid_res)
    
    def test_merge_down_right1(self):
        grid = game.merge_down(self.grid1)

        grid_res = [[0, 0, 0, 0],
                    [0, 0, 0, 2],
                    [2, 2, 0, 32],
                    [16, 4, 8, 32]]

        self.assertEqual(grid, grid_res)




if __name__ == '__main__':
    unittest.main()

