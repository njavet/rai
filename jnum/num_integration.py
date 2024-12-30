import numpy as np


def sum_midpoint(f, a, b, n=1):
    h = (b - a) / n
    x = np.zeros(n + 1)
    y = np.zeros(n)
    x[0] = a

    num_int = 0
    for i in range(n):
        y[i] = f(x[i] + (h/2))
        x[i + 1] = x[i] + h
        num_int += y[i]
    return h * num_int, x, y


def sum_trapezoid(f, a, b, n=1):
    h = (b - a) / n
    x = np.zeros(n + 1)
    y = np.zeros(n + 1)
    x[0] = a
    y[0] = f(a)
    y[-1] = f(b)

    num_int = (y[0] + y[-1]) / 2
    for i in range(1, n):
        x[i] = x[i-1] + h
        y[i] = f(x[i])
        num_int += y[i]
    return h * num_int, x, y


def sum_neq_trapezoid(x, y):
    tf_neq = 0
    for i in range(len(x) - 1):
        tf_neq += ((y[i] + y[i+1]) / 2) * (x[i+1] - x[i])
    return tf_neq


def sum_simpson(f, a, b, n=1):
    h = (b - a) / n
    x = np.zeros(n + 1)
    y = np.zeros(n + 1)
    x[0] = a
    x[-1] = b
    x[-2] = b - h
    y[0] = f(a)
    y[-1] = f(b)

    num_int = 0.5 * (y[0] + y[-1])
    for i in range(1, n):
        x[i] = x[i-1] + h
        num_int += f(x[i])

    for i in range(1, n+1):
        num_int += 2*f((x[i-1] + x[i]) / 2)

    return (h/3) * num_int, x, y


def romberg(f, a, b, m):
    T = {}
    for j in range(m+1):
        T[j, 0], _, _ = sum_trapezoid(f, a, b, 2**j)

    for k in range(1, m+1):
        for j in range(0, m+1-k):
            T[j, k] = ((4**k) * T[j+1, k-1] - T[j, k-1]) / (4**k - 1)
    return T[0, m]


