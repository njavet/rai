
import matplotlib.pyplot as plt
import numpy as np


def f(x, p):
    return np.sin(p[0] + 0.06 * p[1]*x) * np.exp(-(1/32) * (p[0] + 0.06 * p[1] * x) ** 2)


fig, ax = plt.subplots()
