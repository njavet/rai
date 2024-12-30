import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt


class NaturalCubicSpline:
    def __init__(self, x_points, y_points):
        assert len(x_points) == len(y_points)
        self.n = len(x_points) - 1
        self.x_points = x_points
        self.y_points = y_points
        self.h = [self.x_points[i + 1] - self.x_points[i] for i in range(self.n)]
        self.c = np.zeros((4, self.n))
        self.compute_coefficients()

    def __call__(self, x):
        return self.eval_at_x(x)

    def eval_at_x(self, x):
        # out of the interval
        if x < self.x_points[0]:
            dx = x - self.x_points[0]
            y = np.array([dx ** 3, dx ** 2, dx, 1])
            return np.dot(self.c[:, 0], y)
        if self.x_points[-1] < x:
            dx = x - self.x_points[self.n - 1]
            y = np.array([dx ** 3, dx ** 2, dx, 1])
            return np.dot(self.c[:, -1], y)

        for i in range(self.n):
            if self.x_points[i] <= x <= self.x_points[i + 1]:
                dx = x - self.x_points[i]
                y = np.array([dx**3, dx**2, dx, 1])
                return np.dot(self.c[:, i], y)

    def compute_b_i(self, i):
        tmp0 = (self.y_points[i + 1] - self.y_points[i]) / self.h[i]
        try:
            tmp1 = (self.h[i] / 3) * (self.c[1][i + 1] + 2 * self.c[1][i])
        except IndexError:
            tmp1 = (self.h[i] / 3) * 2 * self.c[1][i]
        return tmp0 - tmp1

    def compute_cy_i(self, i):
        tmp0 = 3 * (self.y_points[i+1] - self.y_points[i]) / self.h[i]
        tmp1 = 3 * (self.y_points[i] - self.y_points[i-1]) / self.h[i-1]
        return tmp0 - tmp1

    def compute_d_i(self, i):
        try:
            res = 1 / (3 * self.h[i]) * (self.c[1][i + 1] - self.c[1][i])
        except IndexError:
            res = 1 / (3 * self.h[i]) * (- self.c[1][i])
        return res

    def compute_coefficients(self):
        self.c[3] = self.y_points[:-1]

        if self.n == 2:
            self.c[1][1] = self.compute_cy_i(1) / (2*(self.h[0] + self.h[1]))
        else:
            mat = np.zeros((self.n - 1, self.n - 1))
            mat[0][0:2] = np.array([2*(self.h[0] + self.h[1]), self.h[1]])
            mat[-1][-2:] = np.array([self.h[-1], 2*(self.h[-1] + self.h[-2])])
            cx = np.zeros(self.n - 1)
            cx[0] = self.compute_cy_i(1)
            for i in range(1, self.n-2):
                mat[i, i-1] = self.h[i-1]
                mat[i, i] = 2 * (self.h[i-1] + self.h[i])
                mat[i, i+1] = self.h[i]
                cx[i] = self.compute_cy_i(i+1)
            self.c[1][1:] = np.linalg.solve(mat, cx)

        for i in range(self.n):
            self.c[2][i] = self.compute_b_i(i)
            self.c[0][i] = self.compute_d_i(i)

    def plot_spline(self):
        xmin = np.min(self.x_points) - 1
        xmax = np.max(self.x_points) + 1
        xs = np.arange(xmin, xmax, 0.01)
        ys = [self.eval_at_x(xi) for xi in xs]
        plt.scatter(self.x_points, self.y_points, color='red', label='datapoints')
        cs_ref = CubicSpline(self.x_points, self.y_points, bc_type='natural')
        plt.plot(xs, ys, color='blue', label='spline')
        plt.plot(xs, cs_ref(xs), color='cyan', label='scipy spline')
        plt.legend()
        plt.show()
        

if __name__ == '__main__':
    t = np.array([1900.,
                  1910.,
                  1920.,
                  1930.,
                  1940.,
                  1950.,
                  1960.,
                  1970.,
                  1980.,
                  1990.,
                  2000])

    pt = np.array([75.995,
                   91.972,
                   105.711,
                   123.203,
                   131.669,
                   150.697,
                   179.323,
                   203.212,
                   226.505,
                   249.633,
                   281.422])

    ncs = NaturalCubicSpline(t, pt)
    ncs.plot_spline()

