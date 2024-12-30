"""
regularization for overfitting, lower polynom degree

"""
import numpy as np
import matplotlib.pyplot as plt
from linreg import LinReg



M = 200
rng = np.random.default_rng(0x101)
x = np.sort(2 * rng.random(M) - 1)
noise = rng.normal(loc=0., scale=0.25, size=M)
theta_true = [0.5, 1, 1.5, 0.01]
y_true = 0.5 + x + 1.5*x*x + 0.01 * x ** 3
y = y_true + noise


xr = x.reshape((M, 1))
x1 = np.hstack((xr, xr**2, xr**3))
lr = LinReg()
lr.fit(x1, y)
print('true', theta_true)
print('lin', lr.theta)

ones = np.ones((M, 1))
x2 = np.hstack((ones, x1))
y_pred = lr.predict(x2)

plt.scatter(x, y)
plt.plot(x, y_true, c='r')
plt.plot(x, y_pred, c='g')
plt.show()

