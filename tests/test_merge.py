import unittest
import numpy as np

# project imports
from rai.g2048.expectimax import (merge_up,
                                  merge_down,
                                  merge_left,
                                  merge_right)


class TestMerge(unittest.TestCase):
    def setUp(self):
        self.grid0 = np.array([[2, 2, 2, 2],
                               [4, 4, 0, 0],
                               [2, 4, 8, 16],
                               [2, 0, 2, 4]], dtype=np.float64)

        self.grid1 = np.array([[2, 2, 4, 2],
                               [8, 4, 4, 16],
                               [8, 0, 0, 16],
                               [0, 0, 0, 32]], dtype=np.float64)

    def test_merge_left_grid0(self):
        grid, _ = merge_left(self.grid0)
        grid_res = np.array([[4, 4, 0, 0],
                             [8, 0, 0, 0],
                             [2, 4, 8, 16],
                             [4, 4, 0, 0]], dtype=np.float64)
        self.assertTrue(np.all(grid == grid_res))

    def test_merge_left_grid1(self):
        grid, _ = merge_left(self.grid1)
        grid_res = np.array([[4, 4, 2, 0],
                             [8, 8, 16, 0],
                             [8, 16, 0, 0],
                             [32, 0, 0, 0]], dtype=np.float64)
        self.assertTrue(np.all(grid == grid_res))

    def test_merge_right_grid0(self):
        grid, _ = merge_right(self.grid0)
        grid_res = np.array([[0, 0, 4, 4],
                             [0, 0, 0, 8],
                             [2, 4, 8, 16],
                             [0, 0, 4, 4]], dtype=np.float64)
        self.assertTrue(np.all(grid == grid_res))

    def test_merge_right_grid1(self):
        grid, _ = merge_right(self.grid1)
        grid_res = np.array([[0, 4, 4, 2],
                             [0, 8, 8, 16],
                             [0, 0, 8, 16],
                             [0, 0, 0, 32]], dtype=np.float64)
        self.assertTrue(np.all(grid == grid_res))

    def test_merge_up_grid0(self):
        grid, _ = merge_up(self.grid0)
        grid_res = np.array([[2, 2, 2, 2],
                             [4, 8, 8, 16],
                             [4, 0, 2, 4],
                             [0, 0, 0, 0]], dtype=np.float64)
        self.assertTrue(np.all(grid == grid_res))

    def test_merge_up_grid1(self): 
        grid, _ = merge_up(self.grid1)
        grid_res = np.array([[2, 2, 8, 2],
                             [16, 4, 0, 32],
                             [0, 0, 0, 32],
                             [0, 0, 0, 0]], dtype=np.float64)
        self.assertTrue(np.all(grid == grid_res))

    def test_merge_down_grid0(self):
        grid, _ = merge_down(self.grid0)
        grid_res = np.array([[0, 0, 0, 0],
                             [2, 0, 2, 2],
                             [4, 2, 8, 16],
                             [4, 8, 2, 4]], dtype=np.float64)
        self.assertTrue(np.all(grid == grid_res))

    def test_merge_down_grid1(self):
        grid, _ = merge_down(self.grid1)
        grid_res = np.array([[0, 0, 0, 0],
                             [0, 0, 0, 2],
                             [2, 2, 0, 32],
                             [16, 4, 8, 32]], dtype=np.float64)
        self.assertTrue(np.all(grid == grid_res))


if __name__ == '__main__':
    unittest.main()
