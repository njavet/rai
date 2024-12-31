import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report


X, y = make_moons(n_samples=10000,
                  noise=0.4,
                  random_state=0x101)

colors = ['cyan', 'purple']
fig, ax = plt.subplots(figsize=(7, 3))
for i, cn in enumerate([0, 1]):
    ax.scatter([X[y == i][:, 0]],
               X[y == i][:, 1],
               label=i,
               color=colors[i],
               edgecolor='k')
ax.legend()

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0x101)

