import numpy as np
import sympy as sp


# lagrange interpolation
def lagrange_polynomial(x, x_points, y_points):
    n = len(x_points)
    p = 0 
    for i in range(n):
        p += lagrange_basis_li(i, x, x_points) * y_points[i]
    return p


def lagrange_basis_li(i, x, x_points):
    n = len(x_points) 
    li = 1
    for j in range(n):
        if i != j:
            li *= (x - x_points[j]) / (x_points[i] - x_points[j])
    return li


class LagrangePoly:
    def __init__(self, x_points, y_points):
        sp.init_printing()
        assert len(x_points) == len(y_points)
        self.n = len(x_points) 
        self.x_points = x_points
        self.y_points = y_points
        self.sp_poly = 0
        self.sp_vector = np.zeros(self.n)
        self.f_poly = self.construct_sym_poly()

    def construct_sym_poly(self):
        x = sp.symbols('x')
        self.sp_poly = 0
        self.sp_vector = np.zeros(self.n)
        for i in range(self.n):
            li = sp.simplify(self.li(i, x) * self.y_points[i])
            self.sp_poly += li
        return sp.lambdify(x, self.sp_poly, 'numpy')

    def li(self, i, x):
        res = 1
        for j in range(self.n):
            if i != j:
                res *= (x - self.x_points[j]) / (self.x_points[i] - self.x_points[j])
        return res

    def eval_poly(self, x):
        p = 0 
        for i in range(self.n):
            p += self.li(i, x) * self.y_points[i]
        return p

