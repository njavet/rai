# -*- coding: UTF-8 -*-
import random
import numpy as np

# Author:      chrn (original by Micha Schwendener)
# Date:				 11.11.2016
# Description: Simulate movements on the board without interaction with the browser.
#              This is needed to look ahead 

def merge_right(b):
    """
    Merge the board right
    Args: b (list) two dimensional board to merge
    Returns: list
    >>> merge_right(test)
    [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    """

    def reverse(x):
        return list(reversed(x))

    t = map(reverse, b)
    return np.array([reverse(x) for x in merge_left(t)])

def merge_up(b):
    """
    Merge the board upward. Note that zip(*t) is the
    transpose of b
    Args: b (list) two dimensional board to merge
    Returns: list
    >>> merge_up(test)
    [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    """

    t = merge_left(zip(*b))
    return np.array([list(x) for x in zip(*t)])

def merge_down(b):
    """
    Merge the board downward. Note that zip(*t) is the
    transpose of b
    Args: b (list) two dimensional board to merge
    Returns: list
    >>> merge_down(test)
    [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    """

    t = merge_right(zip(*b))
    return np.array([list(x) for x in zip(*t)])

def merge_left(b):
    """
    Merge the board left
    Args: b (list) two dimensional board to merge
    Returns: list
    """

    def merge(row, acc):
        """
        Recursive helper for merge_left. If we're finished with the list,
        nothing to do; return the accumulator. Otherwise, if we have
        more than one element, combine results of first from the left with right if
        they match. If there's only one element, no merge exists and we can just
        add it to the accumulator.
        Args:
            row (list) row in b we're trying to merge
            acc (list) current working merged row
        Returns: list
        """

        if not row:
            return acc

        x = row[0]
        if len(row) == 1:
            return acc + [x]

        return merge(row[2:], acc + [2*x]) if x == row[1] else merge(row[1:], acc + [x])

    board = []
    for row in b:
        merged = merge([x for x in row if x != 0], [])
        merged = merged + [0]*(len(row)-len(merged))
        board.append(merged)
    return np.array(board)

def move_exists(b):
    """
    Check whether or not a move exists on the board
    Args: b (list) two dimensional board to merge
    Returns: list
    >>> b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    >>> move_exists(b)
    False
    >>> move_exists(test)
    True
    """
    for row in b:
        for x, y in zip(row[:-1], row[1:]):
            if x == y or x == 0 or y == 0:
                return True
    return False
