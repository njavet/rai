import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model 


class LogisticRegression:
    def __init__(self, random_seed=0x101):
        self.rng = np.random.default_rng(random_seed)
        self.theta_ = np.zeros(2)

    def predict(self, x):
        return 1 / (1 + np.exp(-np.dot(self.theta_, x)))

    def fit(self, x, y, alpha=0.01, n_iter=512):
        ones = np.ones((x.size, 1))
        M = x.size
        x_ = np.hstack((ones, x.reshape((x.size, 1))))
        self.theta_ = self.rng.standard_normal(2)

        for _ in range(n_iter):

            grad = np.zeros(2)
            for xi, yi in zip(x_, y):
                grad += (self.predict(xi) - yi) * xi
            grad /= M
            self.theta_ -= alpha * grad


def main():
    x = np.array([100., 233, 150, 280, 80, 320, 135, 93, 224, 178])
    X = np.atleast_2d([100, 233, 150, 280, 80, 320, 135, 93, 224, 178]).T
    y = np.array([0, 1, 1, 1, 0, 1, 1, 0, 1, 0])

    logreg = LogisticRegression()
    logreg.fit(x, y)
    x_plot = np.linspace(min(x), max(x))
    y_plot = [1 / (1 + np.exp(-1*(logreg.theta_[0] + logreg.theta_[1] * xi)))
              for xi in x_plot]
    plt.plot(x_plot, y_plot, c='r')
    print('own', logreg.theta_)
    ones = np.ones((x.size, 1))
    x_ = np.hstack((ones, x.reshape((x.size, 1))))
    print('x=', x_)
    print('x0=', x_[0], 'theta=', logreg.theta_, 'dot', np.dot(x_[0],
                                                               logreg.theta_))

    lr = linear_model.LogisticRegression()
    lr.fit(X, y)
    yhat = lr.predict([[190]])
    yhat_prob = lr.predict_proba([[190]])

    print('sk', lr.intercept_, lr.coef_)
    y_plot = [1 / (1 + np.exp(-1*(lr.intercept_ + lr.coef_[0] * xi)))
              for xi in x_plot]
    plt.plot(x_plot, y_plot)
    plt.show()
    


if __name__ == '__main__':
    main()

