"""
kmeans usage 
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans


X, _ = make_blobs(n_samples=300,
                  centers=4,
                  cluster_std=0.6,
                  random_state=0x101)

fig = plt.figure(figsize=(16, 16))
plt.scatter(X[:, 0], X[:, 1], s=50, label='data')

km = KMeans(n_clusters=4, random_state=0x101)
labels = km.fit_predict(X)

unique_labels = set(labels)
colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

for label, color in zip(unique_labels, colors):
    xy = X[labels == label]
    plt.scatter(xy[:, 0], xy[:, 1], c=[color], edgecolor='k')

plt.show()


