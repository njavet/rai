import numpy as np
import random


class Unit:
    def __init__(self, weights):
        self.weights = weights

    def compute(self, x):
        h = self.weights[0] + np.dot(self.weights[1:], x)
        return np.max(0, h)



class NeuralNetwork:
    def __init__(self, n_iter, random_state=1):
        self.n_iter = n_iter
        self.rgen = np.random.RandomState(random_state)
        self.h1 = Unit(self.rgen.normal(loc=0.0, scale=0.01, size=2))
        self.h2 = Unit(self.rgen.normal(loc=0.0, scale=0.01, size=2))
        self.h3 = Unit(self.rgen.normal(loc=0.0, scale=0.01, size=2))
        self.y = Unit(self.rgen.normal(loc=0.0, scale=0.01, size=4))

    def fit(self, x, y):
        for _ in range(self.n_iter):
            h1 = self.h1.compute(x)
            h2 = self.h2.compute(x)
            h3 = self.h3.compute(x)
            y = self.y.compute(np.array(h1, h2, h3))

    def predict(self, x):
        h1 = self.h1.compute(x)
        h2 = self.h2.compute(x)
        h3 = self.h3.compute(x)
        y = self.y.compute(np.array(h1, h2, h3))
        return y

        







