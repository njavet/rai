"""
neural network training.
"""
import numpy as np


class NN:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.d_in = 2
        self.d_layer = 3
        self.omega0 = self.rng.standard_normal((self.d_layer, self.d_in))
        self.omega1 = self.rng.standard_normal(self.d_layer)

    def activation(self, x):
        return np.maximum(0, x)

    def derivative_activation(self, x):
        return (0. < x).astype(float)

    def forward(self, x):
        h1 = self.activation(np.dot(self.omega0, x))
        return self.activation(np.dot(self.omega1, h1))

    def predict(self, inputs):
        if len(inputs) == 1:
            return self.forward(inputs[0])
        else:
            y = np.array([self.forward(xi) for xi in inputs])

    def fit(self, inputs, targets, alpha=0.1, epochs=8):
        losses = []
        M = len(inputs)
        for _ in range(epochs):

            loss = 0
            for x, y in zip(inputs, targets):
                ypred = self.forward(x)
                loss += (1/(2*M)) * (y - ypred) ** 2

            losses.append(loss)


