import numpy as np


def gauss_newton(g, Dg, lam0, max_iter=8, eps=1e-4):
    i = 0
    lam = np.copy(lam0)
    increment = eps + 1
    err_func = np.linalg.norm(g(lam)) ** 2

    while i < max_iter and eps < increment:
        Q, R = np.linalg.qr(Dg(lam))
        delta = np.linalg.solve(R, np.dot(-Q.T, g(lam))).flatten()
        lam += delta
        err_func = np.linalg.norm(g(lam)) ** 2
        increment = np.linalg.norm(delta)
        i += 1
    return lam, i


def gauss_newton_d(g, Dg, lam0, max_iter=32, eps=1e-5, pmax=4):
    i = 0
    lam = np.copy(lam0)
    increment = eps + 1
    err_func = np.linalg.norm(g(lam)) ** 2

    while i < max_iter and eps < increment:
        Q, R = np.linalg.qr(Dg(lam))
        delta = np.linalg.solve(R, -Q.T.dot(g(lam))).flatten()

        p = 0
        while p <= pmax and err_func <= np.linalg.norm(g(lam + delta / 2**p)) ** 2:
            p += 1
        if p <= pmax:
            lam += delta / 2**p
        else:
            lam += delta

        err_func = np.linalg.norm(g(lam)) ** 2
        increment = np.linalg.norm(delta)
        i += 1
        # print('iteration = ', i)
        # print('lambda = ', lam)
        # print('increment = ', increment)
        # print('error functional = ', err_func)

    return lam, i
