import unittest
import numpy as np
import jnum


class Gauss(unittest.TestCase):
    def setUp(self):
        pass

    def test_3x3_matrix_0(self):
        A = np.array([1, 5, 6, 7, 9, 6, 2, 3, 4], dtype=np.float64).reshape(3, 3)
        b = np.array([29, 43, 20], dtype=np.float64)
        x_true = np.linalg.solve(A, b)
        x = jnum.solve_linear_system(A, b)
        x2 = jnum.Solver(A).solve(b)
        # flops rounding errors
        self.assertTrue(np.all(np.isclose(x, x_true)))
        self.assertTrue(np.all(np.isclose(x2, x_true)))

    def test_3x3_matrix_1(self):
        A = np.array([-1, 1, 1, 1, -3, -2, 5, 1, 4],
                     dtype=np.float64).reshape(3, 3)
        b = np.array([0, 5, 3], dtype=np.float64)
        x_true = np.linalg.solve(A, b)
        x = jnum.solve_linear_system(A, b)
        x2 = jnum.Solver(A).solve(b)
        self.assertTrue(np.all(np.isclose(x2, x_true)))
        self.assertTrue(np.all(np.isclose(x, x_true)))

    def test_3x3_matrix_2(self):
        A = np.array([4, -1, -5, -12, 4, 17, 32, -10, -41], 
                     dtype=np.float64).reshape(3, 3)
        b0 = np.array([-5, 19, -39], dtype=np.float64)
        b1 = np.array([6, -12, 48], dtype=np.float64)
        x_true_0 = np.linalg.solve(A, b0)
        x_true_1 = np.linalg.solve(A, b1)
        x0 = jnum.solve_linear_system(A, b0)
        x1 = jnum.solve_linear_system(A, b1)
        self.assertTrue(np.all(np.isclose(x0, x_true_0)))
        self.assertTrue(np.all(np.isclose(x1, x_true_1)))

    def test_3x3_matrix_3(self):
        A = np.array([2, 7, 3, -4, -10, 0, 12, 34, 9],
                     dtype=np.float64).reshape(3, 3)
        b0 = np.array([25, -24, 107], dtype=np.float64)
        b1 = np.array([5, -22, 42], dtype=np.float64)
        x_true_0 = np.linalg.solve(A, b0)
        x_true_1 = np.linalg.solve(A, b1)
        x0 = jnum.solve_linear_system(A, b0)
        x1 = jnum.solve_linear_system(A, b1)
        self.assertTrue(np.all(np.isclose(x0, x_true_0)))
        self.assertTrue(np.all(np.isclose(x1, x_true_1)))

    def test_3x3_matrix_4(self):
        A = np.array([-2, 5, 4, -14, 38, 22, 6, -9, -27],
                     dtype=np.float64).reshape(3, 3)
        b0 = np.array([1, 40, 75], dtype=np.float64)
        b1 = np.array([16, 82, -120], dtype=np.float64)
        x_true_0 = np.linalg.solve(A, b0)
        x_true_1 = np.linalg.solve(A, b1)
        x0 = jnum.solve_linear_system(A, b0)
        x1 = jnum.solve_linear_system(A, b1)
        self.assertTrue(np.all(np.isclose(x0, x_true_0)))
        self.assertTrue(np.all(np.isclose(x1, x_true_1)))

    def test_8x8_matrix_0(self):
        A = np.array([[-1, 2, 3, 2, 5, 4, 3, -1],
                      [3, 4, 2, 1, 0, 2, 3, 8],
                      [2, 7, 5, -1, 2, 1, 3, 5],
                      [3, 1, 2, 6, -3, 7, 2, -2],
                      [5, 2, 0, 8, 7, 6, 1, 3],
                      [-1, 3, 2, 3, 5, 3, 1, 4],
                      [8, 7, 3, 6, 4, 9, 7, 9],
                      [-3, 14, -2, 1, 0, -2, 10, 5]],
                     dtype=np.float64)
        b = np.array([-11, 103, 53, -20, 95, 78, 131, -26], dtype=np.float64)
        x_true = np.linalg.solve(A, b)
        x = jnum.solve_linear_system(A, b)
        x2 = jnum.Solver(A).solve(b)
        self.assertTrue(np.all(np.isclose(x2, x_true)))
        self.assertTrue(np.all(np.isclose(x, x_true)))

    def test_4x4_matrix(self):
        A = np.array([[1, 2, 3, 4],
                      [5, 6, 7, 8],
                      [9, 10, 11, 12],
                      [13, 14, 15, 16]], dtype=np.float64)


if __name__ == '__main__':
    unittest.main()

