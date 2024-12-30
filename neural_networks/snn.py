"""
understanding deep learning book, shallow neural networks implementation

"""
from typing import Callable
import numpy as np


class SNN:
    """
    only 1-d outputs for now
    """
    def __init__(self,
                 d_layer: int,
                 d_in: int,
                 d_out: int,
                 act: Callable,
                 der_act: Callable,
                 seed: int = 0x101):
        self.d_layer = d_layer
        self.d_in = d_in
        self.d_out = d_out
        self.act = act
        self.der_act = der_act
        self.beta0: np.ndarray | None = None
        self.beta1: np.ndarray | None = None
        self.omega0: np.ndarray | None = None
        self.omega1: np.ndarray | None = None
        self.init_network(seed)

    def init_network(self, seed):
        rng = np.random.default_rng(seed)
        self.beta0 = rng.standard_normal(self.d_layer)
        self.beta1 = np.random.rand()
        self.omega0 = rng.standard_normal(self.d_layer * self.d_in).reshape(
            (self.d_layer, self.d_in)
        )
        self.omega1 = rng.standard_normal(self.d_layer * self.d_out)

    def forward(self, x: np.ndarray):
        h1 = self.act(self.beta0 + np.dot(self.omega0, x))
        return self.beta1 + np.dot(self.omega1, h1)

    def predict(self, inputs):
        y = np.zeros(inputs.shape[0])
        for i, x in enumerate(inputs):
            y[i] = self.forward(x)
        return y

    def fit(self, inputs, targets, alpha=0.01, epochs=512):
        for _ in range(epochs):

            for x, y in zip(inputs, targets):
                # column vectors
                part0 = 2 * (self.forward(x) - y)
                inner = self.beta0 + np.dot(self.omega0, x)
                h1 = self.act(inner)
                h1_der = self.der_act(inner)

                # a simple float
                self.beta1 -= alpha * part0
                # d-in array
                self.beta0 -= alpha * part0 * np.dot(self.omega1, h1_der)
                self.omega1 -= alpha * part0 * h1
                part1 = np.dot(self.omega1, h1_der)
                self.omega0 -= alpha * part0 * part1 * x


def relu(x):
    return np.maximum(0, x)


def relu_derivative(x):
    return (x > 0.).astype(float)


def xor_classifier():
    inputs = np.array([[0., 0.],
                       [0., 1.],
                       [1., 0.],
                       [1., 1.]])
    targets = np.array([0., 1., 1., 0.])
    snn = SNN(d_layer=3,
              d_in=2,
              d_out=1,
              act=relu,
              der_act=relu_derivative)
    snn.fit(inputs, targets)
    print(snn.predict(inputs))


def main():
    pass



if __name__ == '__main__':
    main()
