import numpy as np


def argmax(arr):
    """ randomize return value """
    arr_max = np.max(arr)
    return np.random.choice(np.where(arr == arr_max)[0])
