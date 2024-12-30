import numpy as np


def random_argmax(arr: np.ndarray) -> int:
    """ randomize action selection for ties """
    arr_max = np.max(arr)
    arr_maxes = np.where(arr == arr_max)[0]
    action = int(np.random.choice(arr_maxes))
    return action

