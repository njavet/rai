import random
import numpy as np


class LinReg1D:
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
        self.weights = None

    def fit(self, x, y):
        rgen = np.random.RandomState(self.random_state)
        self.weights = rgen.normal(loc=0.0, scale=0.1, size=2)

        for _ in range(self.n_iter):
            # theta = theta - alpha * derivative(theta)
            for xi, yi in zip(x, y):
                net_input = self.net_input(xi)
                self.weights[0] -= self.eta * 2 * (net_input - yi)
                self.weights[1] -= self.eta * 2 * xi * (net_input - yi) 


    def net_input(self, x):
        return self.weights[0] + self.weights[1] * x 



class Perceptron:
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
        self.weights = None


    def fit(self, X, y):
        rgen = np.random.RandomState(self.random_state)
        self.weights = rgen.normal(loc=0.0, scale=0.01, size=X.shape[1] + 1)

        for _ in range(self.n_iter):
            for xi, y_ref in zip(X, y):
                update = self.learning_rule(xi, y_ref)
                self.weights[1:] += update * xi
                self.weights[0] += update

    def learning_rule(self, xi, y_ref):
        return self.eta * (y_ref - self.predict(xi))

    def net_input(self, x):
        return np.dot(self.weights[1:], x) + self.weights[0]

    def threshold(self, x):
        return np.where(x >= 0.0, 1, -1)

    def predict(self, x):
        return self.threshold(self.net_input(x))


class Adaline:
    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state
        self.weights = None


    def fit(self, X, y):
        rgen = np.random.RandomState(self.random_state)
        self.weights = rgen.normal(loc=0.0, scale=0.01, size=X.shape[1] + 1)

        for _ in range(self.n_iter):
            print(self.weights)
            for xi, y_ref in zip(X, y):
                update = self.eta * (y_ref - self.predict(xi))
                self.weights[1:] += update * xi
                self.weights[0] += update

    def net_input(self, x):
        return np.dot(self.weights[1:], x) + self.weights[0]

    def activation(self, x):
        return x
    
    def threshold(self, x):
        return np.where(x >= 0.0, 1, -1)

    def predict(self, x):
        return self.activation(self.net_input(x))

