import numpy as np
import sympy as sp


# init sympy printing
sp.init_printing()

# define symbols
x1, x2, x3 = sp.symbols('x1 x2 x3')

# define functions
f1 = x1 + x2**2 - x3**2 - 13
f2 = sp.ln(x2/4) + sp.exp(0.5*x3 - 1) - 1
f3 = (x2-3)**2 - x3**3 + 7

# combine defined functions
f = sp.Matrix([f1, f2, f3])

# get jacobian matrix
Df = f.jacobian([x1, x2, x3])

# numpy array
x0 = np.array([1.5, 3, 2.5])

# numerical evaluation with substitution, Matrix type
fx0_0 = f.subs([(x1, 1.5), (x2, 3), (x3, 2.5)])

# get numerical representations of e.g. log(1/2)
fx0_1 = fx0_0.evalf()

# with lambdify, different possibilities to define input parameters
fl0 = sp.lambdify([x1, x2, x3], f, 'numpy')
fx0_2 = fl0(x0[0], x0[1], x0[2])

x = sp.Matrix([x1, x2, x3])
fl1 = sp.lambdify(x, f, 'numpy')
fx0_3 = fl1(x0[0], x0[1], x0[2])

fl2 = sp.lambdify([x], f, 'numpy')
fx0_4 = fl2(x0)

Dfl = sp.lambdify([x], Df, 'numpy')
df0 = Dfl(x0)

# since x is a 3x1 - matrix
xd = x - x0.reshape(-1, 1)
g = fx0_4 + np.dot(df0, xd)

# sp.plot_implicit(sp.Eq(f[0], 0, (x, min, max), (y, min, max))
