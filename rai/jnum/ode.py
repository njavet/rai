"""
coefficients for general runge kutta
euler:
coef_c = [0]
coef_b = [1]
coef_a = [[0, 0], [0, 0]]

midpoint:
coef_c = [0, 0.5]
coef_b = [0, 1]
coef_c = [[0, 0], [0.5, 0]]

modeuler:
coef_c = [0, 1]
coef_b = [0.5, 0.5]
coef_a = [[0, 0], [1, 0]]

classic runge kutte s = 4
coef_c = [0, 0.5, 0.5, 1]
coef_b = [1/6, 1/3, 1/3, 1/6]
coef_a = [[0, 0, 0, 0], [0.5, 0, 0, 0], [0, 0.5, 0, 0], [0, 0, 1, 0]]


"""
import numpy as np


def euler(f, a, b, n, y0):
    h = (b - a) / n
    x = np.zeros(n + 1)
    y = np.zeros(n + 1)
    x[0] = a
    y[0] = y0

    for i in range(n):
        x[i+1] = x[i] + h
        y[i+1] = y[i] + h*f(x[i], y[i])

    return x, y


def midpoint(f, a, b, n, y0):
    h = (b - a) / n
    x = np.zeros(n + 1)
    y = np.zeros(n + 1)
    x[0] = a
    y[0] = y0

    for i in range(n):
        xh2 = x[i] + h/2
        yh2 = y[i] + (h/2)*f(x[i], y[i])
        x[i+1] = x[i] + h
        y[i+1] = y[i] + h*f(xh2, yh2)

    return x, y


def modeuler(f, a, b, n, y0):
    h = (b - a) / n
    x = np.zeros(n + 1)
    y = np.zeros(n + 1)
    x[0] = a
    y[0] = y0

    for i in range(n):
        x[i+1] = x[i] + h
        yi1 = y[i] + h*f(x[i], y[i])
        k1 = f(x[i], y[i])
        k2 = f(x[i+1], yi1)
        y[i+1] = y[i] + (h/2) * (k1 + k2)

    return x, y


def runge_kutta_k4(f, a, b, n, y0):
    h = (b - a) / n
    x = np.zeros(n + 1)
    y = np.zeros(n + 1)
    x[0] = a
    y[0] = y0

    for i in range(n):
        k1 = f(x[i], y[i])
        k2 = f(x[i] + (h/2), y[i] + (h/2)*k1)
        k3 = f(x[i] + (h/2), y[i] + (h/2)*k2)
        k4 = f(x[i] + h, y[i] + h*k3)
        x[i+1] = x[i] + h
        y[i+1] = y[i] + (h/6) * (k1 + 2*k2 + 2*k3 + k4)

    return x, y


def runge_kutta_k4_dn(f, a, b, n, z0):
    h = (b - a) / n
    x = np.zeros(n + 1)
    z = np.zeros((n + 1, z0.size))
    x[0] = a
    z[0] = z0

    for i in range(n):
        k1 = f(x[i], z[i])
        k2 = f(x[i] + (h/2), z[i] + (h/2)*k1)
        k3 = f(x[i] + (h/2), z[i] + (h/2)*k2)
        k4 = f(x[i] + h, z[i] + h*k3)
        x[i+1] = x[i] + h
        z[i+1] = z[i] + (h/6) * (k1 + 2*k2 + 2*k3 + k4)

    return x, z



def runge_kutta_s(f, a, b, n, z0, butcher):
    """
    c1, ..., cs = butcher[:, 0]
    b1, ..., bs = butcher[s-1, :]
    """

    s = butcher.shape[0] - 1
    h = (b - a) / n
    x = np.zeros(n + 1)
    if isinstance(z0, int):
        z = np.zeros(n + 1)
    else:
        z = np.zeros((n + 1, z0.size))

    x[0] = a
    z[0] = z0

    for i in range(n):
        ks = np.zeros(s)
        for j in range(s):
            x_arg = x[i] + butcher[j, 0] * h
            tmp = 0
            for m in range(j):
                tmp += butcher[j, m+1] * ks[m]
            z_arg = z[i] + h * tmp
            ks[j] = f(x_arg, z_arg)

        x[i+1] = x[i] + h
        tmp = 0 
        for m in range(s):
            tmp += butcher[-1, m] * ks[m]
        z[i+1] = z[i] + h * tmp
    return x, z


def general_runge_kutta(f, a, b, n, z0, coef_c, coef_b, coef_a):
    s = len(coef_b)
    assert s == len(coef_c)
    assert coef_a.shape == (s, s)

    h = (b - a) / n
    x = np.zeros(n + 1)
    z = np.zeros((n + 1, z0.size))

    x[0] = a
    z[0] = z0

    for i in range(n):
        ks = np.zeros((s, z0.size))

        for j in range(s):
            x_arg = x[i] + coef_c[j] * h
            z_arg = z[i] + h * np.dot(coef_a[j, :], ks)
            ks[j] = f(x_arg, z_arg)

        x[i+1] = x[i] + h
        z[i+1] = z[i] + h * np.dot(coef_b, ks)

    return x, z
