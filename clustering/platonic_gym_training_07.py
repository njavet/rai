"""
dbscan training
"""

from sklearn.datasets import make_moons
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(32, 10))

X, _ = make_moons(n_samples=256, noise=0.05, random_state=0x101)

km = KMeans(n_clusters=2)
labels = km.fit_predict(X)
unique_labels = set(labels)
colors = ['cyan', 'purple']

ax = fig.add_subplot(1, 4, 1)
ax.set_title('KMeans plot')
for label, color in zip(unique_labels, colors):
    xy = X[labels==label]
    ax.scatter(xy[:, 0], xy[:, 1], color=color, edgecolor='black')
ax.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], color='black',
           marker='x', s=200)


eps_values = [0.2, 0.4, 0.6]
for i, eps in enumerate(eps_values):
    ax = fig.add_subplot(1, 4, i + 2)
    ax.set_title(f'DBSCAN with eps = {eps}')
    dbscan = DBSCAN(min_samples=8, eps=eps)
    labels = dbscan.fit_predict(X)
    unlabs = set(labels)
    if len(unlabs) > 2:
        colors = [plt.cm.Spectral(l) for l in np.linspace(0, 1, len(unlabs))]
    else:
        colors = ['cyan', 'purple']
    for label, color in zip(unlabs, colors):
        xy = X[labels==label]
        ax.scatter(xy[:, 0], xy[:, 1], color=color, edgecolor='black')


plt.show()


