import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk

plt.style.use('cyberpunk')


def runge_kutta_k4(f, a, b, n, y0):
    h = (b - a) / n
    x = np.zeros(n + 1)
    y = np.zeros((n + 1, 2))
    x[0] = a
    y[0] = y0

    for i in range(n):
        k1 = f(x[i], y[i]).flatten()
        k2 = f(x[i] + (h/2), y[i] + (h/2)*k1).flatten()
        k3 = f(x[i] + (h/2), y[i] + (h/2)*k2).flatten()
        k4 = f(x[i] + h, y[i] + h*k3).flatten()
        x[i+1] = x[i] + h
        y[i+1] = y[i] + (h/6) * (k1 + 2*k2 + 2*k3 + k4)

    return x, y



# damping coefficient [Ns/m]
c = 0.16

# mass [kg]
m = 1

# length of the string [m]
l = 1

# free fall [kgm/s^2]
g = 9.81

# initial value
y0 = np.array([np.pi / 2, 0])

# time interval
a = 0
b = 60
n = 6000

t, z1, z2 = sp.symbols('t z1 z2')
p = sp.Matrix([z1, z2])

f = sp.Matrix([z2,
               (-c/m)*z2 - (g/l)*sp.sin(z1)])
f = sp.lambdify([t, p], f, 'numpy')

x, y = runge_kutta_k4(f, a, b, n, y0)


fig = plt.figure(figsize=(16, 12))
ax1 = fig.add_subplot(111)
ax1.set_title('Oscillation')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Distance [m]')
ax1.plot(x, y[:, 0], label='phi')
ax1.plot(x, y[:, 1], label='dphi/dt')
ax1.legend()
ax1.grid()

mplcyberpunk.add_glow_effects()
ax1.grid()
plt.show()

