import functools
import itertools
import operator

import numpy as np
from sklearn.datasets import make_blobs


class MLP:
    def __init__(self, n_hidden, seed=0x101):
        self.rng = np.random.default_rng(seed)
        self.n_hidden = n_hidden
        self.d_in = 0
        self.d_out = 0
        self.b0 = None
        self.b1 = None
        self.w0 = None
        self.w1 = None

    def _init_weights(self):
        self.b0 = np.zeros(self.n_hidden)
        self.b1 = np.zeros(self.d_out)
        self.w0 = self.rng.standard_normal((self.n_hidden, self.d_in))
        self.w1 = self.rng.standard_normal((self.d_out, self.n_hidden))

    @staticmethod
    def relu(x):
        return np.maximum(0, x)

    @staticmethod
    def df_relu(x):
        return (0. < x).astype(float)

    def forward_pass(self, x):
        # z(1) = b(0) + w(0) * a(0)
        z1 = self.b0 + np.dot(self.w0, x)
        # a(1) = relu(z(1))
        a1 = self.relu(z1)
        # z(2) = b(1) + w(1) * a(1)
        z2 = self.b1 + np.dot(self.w1, a1)
        return z1, a1, z2

    def predict(self, x):
        z1 = self.b0 + np.dot(self.w0, x)
        # a(1) = relu(z(1))
        a1 = self.relu(z1)
        # z(2) = b(1) + w(1) * a(1)
        z2 = self.b1 + np.dot(self.w1, a1)
        return z2

    def fit(self, inputs, targets, alpha=0.01, epochs=8):
        n_samples, self.d_in = inputs.shape
        try:
            _, self.d_out = targets.shape
        except ValueError:
            self.d_out = 1
        self._init_weights()

        for _ in range(epochs):

            for xi, yi in zip(inputs, targets):
                z1, a1, z2 = self.forward_pass(xi)

                delta_1 = 2 * (z2 - yi)
                delta_0 = np.dot(np.dot(delta_1, self.w1), self.df_relu(z1))

                self.b1 -= alpha * delta_1
                self.w1 -= alpha * np.dot(delta_1.reshape(-1, 1), a1.reshape(1, -1))

                self.b0 -= alpha * delta_0
                x = np.tile(xi, (self.n_hidden, 1))
                self.w0 -= alpha * delta_0 * x


if __name__ == '__main__':
    x = np.array(list(itertools.product([0, 1], repeat=4)))
    y = []
    for t in x:
        a, b = functools.reduce(operator.and_, t), functools.reduce(operator.or_, t)
        y.append((a, b))
    y = np.array(y)

    X, y = make_blobs(n_samples=300,
                      n_features=2)
    nn = MLP(n_hidden=3)
    nn.fit(X, y)
    print(nn.w0)
    print(nn.w1)
    print(nn.b0)
    print(nn.b1)



