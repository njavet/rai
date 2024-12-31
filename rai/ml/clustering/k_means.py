import numpy as np
import matplotlib.pyplot as plt
import collections
import operator
from sklearn.datasets import make_blobs


class KMeans:
    """
    X: M datapoints x(m) with N features x(m) = (x(m)(1), ... , x(m)(N)
    K: number of clusters
    returns K centroids
    """
    def __init__(self, k):
        self.k = k
        self.X: np.ndarray
        self.m: int = 0
        self.n: int = 0
        self.centroids: np.ndarray
        self.old_centroids = None
        self.clusters = collections.defaultdict(list)
        self.old_clusters = None
        self.centroid_history = None

    def fit(self, X):
        self._init_algorithm(X)
        self.centroid_history = [self.centroids]
        while not np.all(np.equal(self.old_centroids, self.centroids)):
            self._assign_datapoints()
            self._update_centroids()
            self.centroid_history.append(self.centroids)
        print('old', self.old_centroids)
        print('new', self.centroids)

    def _init_algorithm(self, X):
        self.X = X
        try:
            self.m, self.n = X.shape
        except ValueError:
            raise Exception('wrong array shape')
        random_ind = np.random.choice(self.m, self.k, replace=False)
        self.centroids = self.X[random_ind]

    def _assign_datapoints(self):
        # for each datapoint compute the closest centroid and assign datapoint
        # to this cluster
        self.old_clusters = self.clusters
        self.clusters = collections.defaultdict(list)
        for x in self.X:
            dists = []
            for i, ci in enumerate(self.centroids):
                d = np.sqrt(np.sum(np.square(x - ci)))
                dists.append((i, d))
            closest_centroid, _ = sorted(dists, key=operator.itemgetter(1))[0]
            self.clusters[closest_centroid].append(x)

    def _update_centroids(self):
        self.old_centroids = self.centroids
        for i, ck in enumerate(self.old_centroids):
            mk = (1 / len(self.clusters[i])) * np.sum(self.clusters[i], axis=0)
            self.centroids[i] = mk


def main():
    X, _ = make_blobs(n_samples=16, centers=4, random_state=0x101)
    plt.scatter(X[:, 0], X[:, 1], label='data points')
    km = KMeans(k=4)
    km.fit(X)
    for i, centroid in enumerate(km.centroid_history):
        plt.scatter(centroid[:, 0], centroid[:, 1], label=str(i))
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
