"""
newton method for systems (O(n**2), f 3xcon differentiable, Df regular, x0
close)
 can converge to local minima != 0 => Df not regular
select start vector close to solution

1D
f(x1) = f(x0) + f'(x0) * (x1 - x0)
x1 = x0 - f(x0) / f'(x0)

multivariate
f(x1) = f(x0) + Df(x0) * (x1 - x0)
x1 = x0 - Df(x0).inv * f(x0)

d0 = -Df(x0).inv * f(x0)
solve linear system
Df(x0) * d0 = -f(x0)
x1 = x0 + d0
"""
import numpy as np


def newton(f, df, x0, max_iter=32, eps=1e-5, termcond='iter'):
    x0_ = np.copy(x0)

    for i in range(max_iter):
        print(f'x{i} = {x0_}')
        d0 = np.linalg.solve(df(x0_), -f(x0_)).flatten()
        xn = x0_ + d0

        # stop criteria
        xdiff_norm = np.linalg.norm(xn - x0_)
        cond0 = xdiff_norm <= np.linalg.norm(xn) * eps
        cond1 = xdiff_norm <= eps
        cond2 = np.linalg.norm(f(xn)) <= eps
        if termcond == 'xdiff' and cond0:
            print('cond0 reached, xn = ', xn)
            return xn
        if termcond == 'xdiff1' and cond1:
            print('cond1 reached, xn = ', xn)
            return xn
        if termcond == 'fnorm' and cond2:
            print('cond2 reached, xn = ', xn)
            return xn
        x0_ = xn

    return x0_


def newton_d(f, df, x0, max_iter=32, kmax=4, eps=1e-5, termcond='iter'):
    x0_ = np.copy(x0)

    for i in range(max_iter):
        print(f'x{i} = {x0_}')
        delta = np.linalg.solve(df(x0_), -f(x0_)).flatten()

        fnorm = np.linalg.norm(f(x0_), 2)
        # if no k will be found
        d0 = np.copy(delta)
        xn = x0_ + delta
        k = 0
        while k <= kmax and np.linalg.norm(f(xn), 2) < fnorm:
            delta /= 2
            xn = x0_ + delta
            k += 1
        if k > kmax:
            xn = x0_ + d0

        xdiff_norm = np.linalg.norm(xn - x0_)
        cond0 = xdiff_norm <= np.linalg.norm(xn) * eps
        cond1 = xdiff_norm <= eps
        cond2 = np.linalg.norm(f(xn)) <= eps
        if termcond == 'xdiff' and cond0:
            print('cond0 reached, xn = ', xn)
            return xn
        if termcond == 'xdiff1' and cond1:
            print('cond1 reached, xn = ', xn)
            return xn
        if termcond == 'fnorm' and cond2:
            print('cond2 reached, xn = ', xn)
            return xn
        x0_ = xn

    return x0_

