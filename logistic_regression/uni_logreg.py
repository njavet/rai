import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


class UnivariateLogisticRegression:
    def __init__(self, random_seed=0x101):
        self.rng = np.random.default_rng(random_seed)
        self.theta_ = self.rng.standard_normal(2)

    def predict(self, x: float) -> float:
        z = self.theta_[0] + self.theta_[1] * x
        return 1 / (1 + np.exp(-z))

    def fit(self, 
            X: np.ndarray,
            y: np.ndarray,
            alpha: float = 0.001,
            n_iter: int = 1512) -> None:

        M = len(X)

        for _ in range(n_iter):

            # compute gradient
            grad = np.zeros(2)
            for xi, yi in zip(X, y):
                y_hat = self.predict(xi)
                grad[0] += (y_hat - yi)
                grad[1] += (y_hat - yi) * xi
            grad /= M

            # update theta
            self.theta_ -= alpha * grad



if __name__ == '__main__':
    ulr = UnivariateLogisticRegression()

    x = np.array([100, 233, 150, 280, 80, 320, 135, 93, 224, 178])
    y = np.array([0, 1, 1, 1, 0, 1, 1, 0, 1, 0])

    ulr.fit(x, y)

    x_plot = np.linspace(min(x), max(x))
    y_plot = [ulr.predict(xi) for xi in x_plot]
    plt.plot(x_plot, y_plot, c='r')
    print('own theta', ulr.theta_)

    lr = LogisticRegression()
    x = np.atleast_2d([100, 233, 150, 280, 80, 320, 135, 93, 224, 178]).T
    lr.fit(x, y)

    print('sk theta', lr.intercept_, lr.coef_)
    y_plot = [lr.predict(xi.reshape(-1, 1)) for xi in x_plot]
    plt.plot(x_plot, y_plot)
    plt.show()
    

