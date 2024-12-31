
"""
clustering training
what if a centroid never gets assigned any points ?
 forgy method -> clustering depends on random centroids
 will not change anymore due to sparse regions

"""

import numpy as np
import matplotlib.pyplot as plt
import operator
import collections
from sklearn.datasets import make_blobs


X, _ = make_blobs(n_samples=300,
                  n_features=2,
                  cluster_std=0.8,
                  centers=4,
                  random_state=0x101)


# number of clusters
K = 4

# choose random datapoints as centroids -> forgy method
indices = np.random.choice(len(X), K)
centroids = X[indices]

# plot
fig = plt.figure(figsize=(28, 16))
colors = ['cyan', 'purple', 'green', 'orange']

# dict for datapoint index to cluster number
for n_iter in range(4):
    ax = fig.add_subplot(2, 4, n_iter + 1)
    ax.grid()
    ax.scatter(centroids[:, 0], 
               centroids[:, 1], 
               color='red',
               label='centroids', 
               zorder=5)

    # compute distance to each centroid and assign point to nearest centroid
    c2p = collections.defaultdict(list)
    for i, p in enumerate(X):
        dists = [] 
        for c_ind, c in enumerate(centroids):
            dists.append((c_ind, np.linalg.norm(p - c, 2)))
        cluster, dist = sorted(dists, key=operator.itemgetter(1))[0]
        c2p[cluster].append(i)

    for cluster_ind, point_inds in c2p.items():
        ax.scatter(X[point_inds][:, 0], 
                   X[point_inds][:, 1],
                   color=colors[cluster_ind],
                   label=str(cluster_ind))
        centroids[cluster_ind] = np.mean(X[point_inds], axis=0)


plt.legend()
plt.show()


