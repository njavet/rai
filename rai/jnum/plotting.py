import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl



def plot_direction_field(f, xmin, xmax, ymin, ymax, hx, hy, ax=None):
    xs = np.arange(xmin, xmax + hx, hx)
    ys = np.arange(ymin, ymax + hy, hy)

    [X, Y] = np.meshgrid(xs, ys)
    Ydiff = f(X, Y)
    Xdiff = np.ones_like(Ydiff)

    if ax is None:
        plt.quiver(X, Y, Xdiff, Ydiff)
        plt.show()
    else:
        ax.quiver(X, Y, Xdiff, Ydiff)


