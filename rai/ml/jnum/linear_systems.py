import timeit
from functools import wraps


def input_check(func):
    @wraps(func)
    def check(A, b):
        try:
            m, n = A.shape
        except ValueError:
            raise Exception('input must be a square 2d array')
        if m != n:
            raise Exception('input must be a square 2d array')
        try:
            mb, nb = b.shape
        except ValueError:
            raise Exception(f'{b} must be a {n} x 1 vector')
        if mb != n and nb != 1:
            raise Exception(f'{b} must be a {n} x 1 vector')
        return func(A, b)
    return check


class Solver:
    def __init__(self, A):
        self.P, self.L, self.U = self.lu_dec_with_pivoting(A)

    def lu_dec_with_pivoting(self, A):
        n = A.shape[0]
        L = np.eye(n)
        P = np.eye(n)
        U = np.copy(A)
        for i in range(n-1):
            max_ind = np.argmax(np.abs(U[i:, i]))
            P[[i, max_ind + i]] = P[[max_ind + i, i]]
            U[[i, max_ind + i]] = U[[max_ind + i, i]]
            L[[i, max_ind + i]] = L[[max_ind + i, i]]
            for j in range(i+1, n):
                L[j, i] = U[j, i] / U[i, i]
                U[j] = U[j] - L[j, i] * U[i]
        return P, L, U

    def solve(self, b):
        y = forward_substitution(self.L, np.dot(self.P, b))
        return backward_substitution(self.U, y)


def solve_linear_system(A, b):
    L, U = lu_decomposition_without_pivoting(A)
    y = forward_substitution(L, b)
    return backward_substitution(U, y)


def lu_decomposition_without_pivoting(A):
    n = A.shape[0]
    L = np.eye(n)
    U = np.copy(A)
    for i in range(n-1):
        for j in range(i+1, n):
            L[j, i] = U[j, i] / U[i, i]
            U[j] = U[j] - L[j, i] * U[i]
    return L, U


@input_check
def gauss_without_pivoting(A, b):
    Aext = np.hstack((A, b))
    n = A.shape[0]
    for i in range(n-1):
        for j in range(i+1, n):
            fac = Aext[j, i] / Aext[i, i]
            Aext[j] = Aext[j] - fac*Aext[i]
    return backward_substitution(Aext[:, 0:n], Aext[:, n])


def forward_substitution(L, b):
    n = L.shape[0]
    y = np.zeros_like(b)
    for i in range(n):
        y[i] = b[i] - np.dot(y[0:i], L[i, 0:i])
    return y


def backward_substitution(R, y):
    n = R.shape[0]
    x = np.zeros_like(y)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(x[i+1:], R[i, i+1:])) / R[i, i]
    return x


def matrix_check(func):
    @wraps(func)
    def check(A):
        if not len(A.shape) == 2:
            raise Exception('NOT A 2D array')
        elif not A.shape[0] == A.shape[1]:
            raise Exception('Not a square matrix')
        else:
            return func(A)
    return check


flo = {}

def lu_decomposition_benchmark(A):
    n = A.shape[0]
    U = np.copy(A)
    L = np.eye(n)
    flops = 0
    for i in range(n-1):
        for j in range(i+1, n):
            L[j, i] = U[j, i] / U[i, i]
            flops += 1
            tmp = L[j, i] * U[i]
            flops += n
            U[j] = U[j] - tmp
            flops += n
    if n in flo:
        flo[n] += flops
        flo[n] /= 2
    else:
        flo[n] = flops
    return L, U


def generate_permutation_matrix(n):
    L = np.tril(np.random.rand(n, n) - 1) + np.eye(n)
    U = np.triu(np.random.rand(n, n))
    return np.dot(L, U)


if __name__ == '__main__':
    setup = "from __main__ import lu_decomposition_benchmark"

    for n in [10, 100, 1000, 10000]:
        A = generate_permutation_matrix(n)
        args = {'A': A}
        e_time = timeit.timeit(stmt="lu_decomposition_benchmark(A)",
                               setup=setup,
                               globals=args,
                               number=1)
        print(f'n = {n}, flops = {flo[n]}, {e_time:.4f} sec')

import numpy as np


def jacobi(A, b, x0):
    L = np.tril(A)
    np.fill_diagonal(L, 0)
    Dinv = np.diag(1 / np.diag(A))
    R = np.triu(A)
    np.fill_diagonal(R, 0)

    for _ in range(5):
        xn = -np.dot(Dinv, np.dot(L + R, x0)) + np.dot(Dinv, b)
        x0 = xn
        print(f'{xn}')
    return xn

