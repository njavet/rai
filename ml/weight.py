import neurons
import numpy as np
import matplotlib.pyplot as plt


data = [(1, 95.0),
        (2, 94.2),
        (3, 94.3),
        (4, 95.2), 
        (5, 95.2), 
        (6, 95.0), 
        (7, 95.0), 
        (8, 95.4), 
        (9, 94.4), 
        (10, 95.5), 
        (11, 96.1), 
        (12, 95.9), 
        (13, 95.3), 
        (14, 95.2), 
        (15, 96.6), 
        (16, 96.1), 
        (17, 96.5), 
        (18, 96.2), 
        (19, 95.8), 
        (20, 95.0), 
        (21, 94.9), 
        (22, 95.8), 
        (23, 96.3), 
        (24, 96.6), 
        (25, 95.2), 
        (26, 95.2), 
        (27, 95.5), 
        (28, 96.1), 
        (29, 95.6), 
        (30, 95.7), 
        (31, 96.4), 
        (32, 96.0), 
        (33, 95.4), 
        (34, 94.7), 
        (35, 95.9)]

# y = ax + b 
# least square loss

fig, ax = plt.subplots()

x = np.array([t[0] for t in data], dtype=np.float64)
y = np.array([t[1] for t in data], dtype=np.float64)

ppn = neurons.LinReg1D()
ppn.fit(x, y)
print(ppn.weights[0], ppn.weights[1])

z = [ppn.net_input(x) for x in range(1, 36)]

ax.plot(y, '*')
ax.plot(z, '-')
ax.set_ylim(90, 100)
plt.show()

