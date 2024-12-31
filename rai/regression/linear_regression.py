import numpy as np
import matplotlib.pyplot as plt


class LinearRegression:
    """
    multivariate linear regression: Rn -> R
    """
    def __init__(self, random_state=0x101):
        self.rng = np.random.default_rng(random_state)
        self.m: int = 0
        self.n: int = 0
        self.theta = None

    def predict(self, x):
        return np.dot(self.theta, x)

    def fit(self, X, y, alpha=.1, n_iter=512):
        # TODO error check
        self.m, self.n = X.shape
        self.theta = self.rng.standard_normal(self.n + 1)
        ones = np.ones((self.m, 1))
        x_ext = np.hstack((ones, X))

        for _ in range(n_iter):
            grad = np.zeros(self.n + 1)
            for xi, yi in zip(x_ext, y):
                grad += (self.predict(xi) - yi) * xi
            grad /= self.m

            self.theta -= alpha * grad


def main():
    lr = LinearRegression()

    M = 101
    rng = np.random.default_rng(0x101)
    x = np.linspace(-1, 1, M)
    noise = rng.normal(loc=0., scale=0.25, size=M)
    theta0 = .5
    theta1 = 2
    y = theta0 + (theta1 * x) + noise

    lr.fit(x.reshape(-1, 1), y)
    print('theta', lr.theta)

    plt.scatter(x, y)
    plt.plot(x, (theta0 + theta1*x), color='green', label='true function')
    plt.plot(x, (lr.theta[0] + lr.theta[1]*x), color='cyan', label='iter')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
