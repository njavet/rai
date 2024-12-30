"""
matrix from, residual plot
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

n_samples = 101
xs = np.linspace(0, 8, n_samples)
rng = np.random.default_rng(0x101)
theta0 = 0.8
theta1 = 6.4
y_true = theta0 + theta1 * xs

y_noise = y_true + rng.standard_normal(n_samples)

lr = LinearRegression()
lr.fit(xs.reshape(-1, 1), y_noise)

residuals = []
for xi, yi in zip(xs, y_noise):
    res = lr.intercept_ + lr.coef_[0] * xi - yi
    residuals.append(res)


fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(32, 16))
ax0.set_title('Data plot')
ax0.scatter(xs, y_noise)
ax0.plot(xs, lr.intercept_ + lr.coef_[0] * xs, color='red')
ax1.scatter(xs, residuals)
for xi, ri in zip(xs, residuals):
    ax1.plot([xi, xi], [0, ri], linestyle='--', color='gray')
    ax1.scatter(xi, ri, zorder=5, color='red')

ax1.grid()
ax1.axvline(0, color='black', linewidth=2)
ax1.axhline(0, color='black', linewidth=2)
print('residual sum', sum(residuals))
plt.show()



