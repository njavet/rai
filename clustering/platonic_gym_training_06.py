""" 
silhouette score
"""
from sklearn.cluster import KMeans
import operator
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


X, _ = make_blobs(n_samples=300,
                  centers=4,
                  cluster_std=0.6,
                  random_state=0x101)


fig = plt.figure(figsize=(32, 20))
silhouette_scores = []

for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=0x101)
    labels = km.fit_predict(X)
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(label) for label in np.linspace(0, 1,
                                                            len(unique_labels))]
    sc = silhouette_score(X, labels)
    silhouette_scores.append((k, sc))



ax = fig.add_subplot(1, 2, 1)
ax.set_title(f'Silhouette plot')

ks, scs = zip(*silhouette_scores)
ax.grid()
ax.plot(ks, scs, marker='*', linestyle='-')
ax.set_xlabel('Number of clusters')
ax.set_ylabel('Silhouette Score')

k, _ = sorted(silhouette_scores, key=operator.itemgetter(1), reverse=True)[0]
ax = fig.add_subplot(1, 2, 2)
km = KMeans(n_clusters=k, random_state=0x101)
labels = km.fit_predict(X)
unique_labels = set(labels)
centroids = km.cluster_centers_
colors = [plt.cm.Spectral(label) for label in np.linspace(0, 1, len(unique_labels))]

for label, color in zip(unique_labels, colors):
    xy = X[labels==label]
    ax.scatter(xy[:, 0], xy[:, 1], color=color, edgecolor='black', s=50, label=f'cluster {label}')

ax.scatter(centroids[:, 0], centroids[:, 1], s=300, linewidth=3, label='centroids', color='black')

plt.show()



