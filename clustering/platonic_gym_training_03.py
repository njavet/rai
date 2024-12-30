"""
    kmeans++ training

"""
import numpy as np
from sklearn.datasets import make_blobs
import collections
import matplotlib.pyplot as plt


X, _ = make_blobs(n_samples=300,
                  n_features=4,
                  cluster_std=0.8,
                  centers=4,
                  random_state=0x101)

K = 4
fig = plt.figure(figsize=(32, 16))

colors = ['cyan', 'purple', 'orange', 'green']
# centroids initialization
index = np.random.choice(len(X))
centroid_inds = [index]
centroids = [X[index]]
for centroid_ind in range(K-1):
    prev_centroid = centroids[-1]
    distances = []
    for i, data_point in enumerate(X):
        dist = np.linalg.norm(data_point - prev_centroid, 2)
        if i not in centroid_inds:
            distances.append((dist, i))

    dis = sorted(distances, reverse=True)[:8]
    _, p_ind = dis[np.random.choice(8)]


    centroids.append(X[p_ind])
    centroid_inds.append(p_ind)
centroids = np.array(centroids)


for n_iter in range(8):
    old_centroids = np.copy(centroids)
    ax = fig.add_subplot(2, 4, n_iter + 1)
    ax.grid()

    c2p = collections.defaultdict(list)
    for i, p in enumerate(X):

        dists = []
        for c_ind, c in enumerate(centroids):
            d = np.linalg.norm(p - c, 2)
            dists.append((d, c_ind))
        _, ci = sorted(dists)[0]
        c2p[ci].append(i)

    for ci, pis in c2p.items():
        data_points = X[pis]
        ax.scatter(data_points[:, 0], 
                   data_points[:, 1], 
                   color=colors[ci],
                   label=str(ci))
        centroids[ci] = np.mean(data_points, axis=0)

    ax.scatter(old_centroids[:, 0], 
               old_centroids[:, 1], 
               c='black', 
               label='centroids',
               linewidths=3,
               marker='x',
               s=200)


plt.legend()
plt.show()
