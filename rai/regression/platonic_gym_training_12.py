"""
like 11, own implementation
batch size 1 -> gradient gets updated with every sample
"""
import numpy as np
import matplotlib.pyplot as plt


n_samples = 101
xs = np.linspace(0, 8, n_samples)
rng = np.random.default_rng(0x101)
theta0 = 1.6
theta1 = 3.2

y_true = theta0 + theta1 * xs
y_noise = y_true + rng.standard_normal(n_samples)


def fit(inputs, targets, alpha=0.01, epochs=512):
    # init weights
    weights = rng.standard_normal(2)
    for _ in range(epochs):
        for xi, yi in zip(inputs, targets):
            xext = np.array([1, xi])
            delta0 = 2 * (np.dot(weights, xext) - yi)
            weights -= alpha * delta0 * xext
    return weights


weights = fit(xs, y_noise)
plt.scatter(xs, y_noise)
plt.plot(xs, weights[0] + weights[1] * xs, c='r')
print('b', weights[0])
print('w', weights[1])

plt.show()
