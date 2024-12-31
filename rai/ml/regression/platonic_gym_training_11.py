"""
given a affine univariate function, use sklearn and find
a fitting curve
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(0x101)

n_samples = 101
theta0 = 1
theta1 = 1.5
xs = np.linspace(0, 8, n_samples)
y_true = theta0 + theta1 * xs
y_noise = y_true + rng.standard_normal(n_samples)


lr = LinearRegression()
lr.fit(xs.reshape(-1, 1), y_noise)
plt.scatter(xs, y_noise)
t0 = lr.intercept_
t1 = lr.coef_[0]
plt.plot(xs, t0 + t1 * xs)
plt.show()
