import numpy as np
import matplotlib.pyplot as plt


class UnivariateLinearRegression:
    def __init__(self, random_seed=0x101):
        self.rng = np.random.default_rng(random_seed)
        self.theta_ = self.rng.standard_normal(2)

    def predict(self, x: float) -> float:
        return self.theta_[0] + self.theta_[1] * x

    def fit(self, 
            X: np.ndarray, 
            y: np.ndarray,
            alpha: float = 0.01,
            n_iter: int = 512) -> None:

        self.theta_ = self.rng.standard_normal(2)
        M = len(X)
        for _ in range(n_iter):

            # compute gradient 
            grad = np.zeros(2)
            for xi, yi in zip(X, y):
                y_hat = self.predict(xi)
                grad[0] += y_hat - yi
                grad[1] += (y_hat - yi) * xi
            grad /= M

            # update theta
            self.theta_ -= alpha * grad


def main():
    ulr = UnivariateLinearRegression()
    M = 101
    x = 2 * ulr.rng.random(M) - 1
    theta0 = 1
    theta1 = 2
    y_true = theta0 + theta1 * x

    noise = ulr.rng.standard_normal(M)
    y = y_true + noise
    plt.scatter(x, y)
    plt.plot(x, y_true, c='r')

    ulr.fit(x, y)
    y_hat = ulr.theta_[0] + ulr.theta_[1] * x
    plt.plot(x, y_hat, c='g')
    plt.show()


if __name__ == '__main__':
    main()
