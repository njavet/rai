import unittest
import game


class TestMerge(unittest.TestCase):
    def setUp(self):

        grid0 = [[2, 2, 2, 2],
                 [4, 4, 0, 0],
                 [2, 4, 8, 16],
                 [2, 0, 2, 4]]

        grid1 = [[2, 2, 4, 2],
                 [8, 4, 4, 16],
                 [8, 0, 0, 16],
                 [0, 0, 0, 32]]

        self.grid2048_0 = game.Grid2048(grid0)
        self.grid2048_1 = game.Grid2048(grid1)

    def test_merge_left_grid0(self):
        # grid = game.merge_left(self.grid0)
        self.grid2048_0.merge_left()

        grid_res = [[4, 4, 0, 0],
                    [8, 0, 0, 0],
                    [2, 4, 8, 16],
                    [4, 4, 0, 0]]

        self.assertEqual(self.grid2048_0.grid, grid_res)

    def test_merge_left_score_grid0(self):
        self.grid2048_0.merge_left()
        self.assertEqual(self.grid2048_0.merge_score, 10)


    def test_merge_left_grid1(self):
        # grid = game.merge_left(self.grid1)
        self.grid2048_1.merge_left()

        grid_res = [[4, 4, 2, 0],
                    [8, 8, 16, 0],
                    [8, 16, 0, 0],
                    [32, 0, 0, 0]]

        self.assertEqual(self.grid2048_1.grid, grid_res)

    def test_merge_left_score_grid1(self):
        self.grid2048_1.merge_left()
        self.assertEqual(self.grid2048_1.merge_score, 6)

    def test_merge_right_grid0(self):
        # grid = game.merge_right(self.grid0)
        self.grid2048_0.merge_right()

        grid_res = [[0, 0, 4, 4],
                    [0, 0, 0, 8],
                    [2, 4, 8, 16],
                    [0, 0, 4, 4]]
        self.assertEqual(self.grid2048_0.grid, grid_res)

        # self.assertEqual(grid, grid_res)

    def test_merge_right_score_grid0(self):
        self.grid2048_0.merge_right()
        self.assertEqual(self.grid2048_0.merge_score, 10)

    def test_merge_right_grid1(self):
        # grid = game.merge_right(self.grid1)
        self.grid2048_1.merge_right()

        grid_res = [[0, 4, 4, 2],
                    [0, 8, 8, 16],
                    [0, 0, 8, 16],
                    [0, 0, 0, 32]]

        #self.assertEqual(grid, grid_res)
        self.assertEqual(self.grid2048_1.grid, grid_res)

    def test_merge_right_score_grid1(self):
        self.grid2048_1.merge_right()
        self.assertEqual(self.grid2048_1.merge_score, 6)

    def test_merge_up_grid0(self): 
        self.grid2048_0.merge_up()
        # grid = game.merge_up(self.grid0)

        grid_res = [[2, 2, 2, 2],
                    [4, 8, 8, 16],
                    [4, 0, 2, 4],
                    [0, 0, 0, 0]]

        self.assertEqual(self.grid2048_0.grid, grid_res)
        # self.assertEqual(grid, grid_res)

    def test_merge_up_score_grid0(self):
        self.grid2048_0.merge_up()
        self.assertEqual(self.grid2048_0.merge_score, 6)

    def test_merge_up_grid1(self): 
        # grid = game.merge_up(self.grid1)
        self.grid2048_1.merge_up()

        grid_res = [[2, 2, 8, 2],
                    [16, 4, 0, 32],
                    [0, 0, 0, 32],
                    [0, 0, 0, 0]]

        # self.assertEqual(grid, grid_res)
        self.assertEqual(self.grid2048_1.grid, grid_res)

    def test_merge_up_score_grid1(self):
        self.grid2048_1.merge_up()
        self.assertEqual(self.grid2048_1.merge_score, 28)

    def test_merge_down_grid0(self):
        # grid = game.merge_down(self.grid0)
        self.grid2048_0.merge_down()

        grid_res = [[0, 0, 0, 0],
                    [2, 0, 2, 2],
                    [4, 2, 8, 16],
                    [4, 8, 2, 4]]

        self.assertEqual(self.grid2048_0.grid, grid_res)
        # self.assertEqual(grid, grid_res)
    def test_merge_down_score_grid0(self):
        self.grid2048_0.merge_down()
        self.assertEqual(self.grid2048_0.merge_score, 6)
    
    def test_merge_down_grid1(self):
        # grid = game.merge_down(self.grid1)
        self.grid2048_1.merge_down()

        grid_res = [[0, 0, 0, 0],
                    [0, 0, 0, 2],
                    [2, 2, 0, 32],
                    [16, 4, 8, 32]]

        # self.assertEqual(grid, grid_res)
        self.assertEqual(self.grid2048_1.grid, grid_res)

    def test_merge_down_score_grid1(self):
        self.grid2048_1.merge_down()
        self.assertEqual(self.grid2048_1.merge_score, 28)




if __name__ == '__main__':
    unittest.main()

