import unittest
import sympy as sp
import numpy as np
import jnum


class TestNewton0(unittest.TestCase):
    def setUp(self):
        self.x = sp.symbols('x0 x1')
        f = sp.Matrix([2*self.x[0] + 4*self.x[1],
                       4*self.x[0] + 8*self.x[1]**3])
        df = f.jacobian(self.x)
        self.f = sp.lambdify([self.x], f, 'numpy')
        self.df = sp.lambdify([self.x], df, 'numpy')
        self.x0 = np.array([4, 2])

    def test_one_iteration(self):
        xn = jnum.newton(self.f, self.df, self.x0, max_iter=1)
        cond = np.isclose(xn, np.array([-2.90909091,
                                        1.45454545]))
        self.assertTrue(np.all(cond))

    def test_two_iterations(self):
        xn = jnum.newton(self.f, self.df, self.x0, max_iter=2)
        cond = np.isclose(xn, np.array([-2.30209358,
                                        1.15104679]))
        self.assertTrue(np.all(cond))

    def test_three_iterations(self):
        xn = jnum.newton(self.f, self.df, self.x0, max_iter=3)
        cond = np.isclose(xn, np.array([-2.05065186,
                                        1.02532593]))
        self.assertTrue(np.all(cond))

    def test_four_iterations(self):
        xn = jnum.newton(self.f, self.df, self.x0, max_iter=4)
        cond = np.isclose(xn, np.array([-2.0018169,
                                        1.00090845]))
        self.assertTrue(np.all(cond))


class TestNewton1(unittest.TestCase):
    def setUp(self):
        self.x = sp.symbols('x0 x1')
        f = sp.Matrix([20 - 18*self.x[0] - 2*self.x[1]**2,
                       -4*self.x[1] * (self.x[0] - self.x[1]**2)])
        df = f.jacobian(self.x)
        self.f = sp.lambdify([self.x], f, 'numpy')
        self.df = sp.lambdify([self.x], df, 'numpy')
        self.x0 = np.array([1.1, 0.9])

    def test_one_iteration_with_norm(self):
        xn = jnum.newton(self.f, self.df, self.x0, max_iter=1)
        cond0 = np.isclose(np.linalg.norm(self.f(self.x0)), 1.7624800708093145)
        self.assertTrue(cond0)
        cond1 = np.isclose(np.linalg.norm(self.x0 - xn), 0.16327880407243942)
        self.assertTrue(cond1)
        cond2 = np.isclose(xn, np.array([0.99594555,
                                         1.02582781]))
        self.assertTrue(np.all(cond2))
        cond3 = np.isclose(np.linalg.norm(self.f(xn)), 0.23349016523989502)
        self.assertTrue(cond3)

    def test_two_iterations_with_norm(self):
        xn = jnum.newton(self.f, self.df, self.x0, max_iter=2)
        cond2 = np.isclose(xn, np.array([0.99986314,
                                         1.00092549]))
        self.assertTrue(np.all(cond2))


class TestNewtonDamped(unittest.TestCase):
    def setUp(self):
        x = sp.symbols('x0 x1 x2')
        f = sp.Matrix([x[0] + x[1]**2 - x[2]**2 - 13,
                       sp.ln(x[1]/4) + sp.exp(0.5*x[2] - 1) - 1,
                       (x[1] - 3)**2 - x[2]**3 + 7])
        df = f.jacobian(x)
        self.f = sp.lambdify([x], f, 'numpy')
        self.df = sp.lambdify([x], df, 'numpy')
        self.x0 = np.array([1.5, 3, 2.5])

    def test_eps_iteration(self):
        eps = 1e-5
        xn = jnum.newton_d(self.f, self.df, self.x0, eps=eps, termcond='fnorm')
        cond0 = np.all(np.isclose(xn, np.array([1.0000001, 4., 2.])))
        self.assertTrue(cond0)


if __name__ == '__main__':
    unittest.main()





