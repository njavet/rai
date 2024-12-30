import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs


class DBSCAN:
    def __init__(self, min_pts: int, eps: float) -> None:
        self.min_pts: int = min_pts
        self.eps: float = eps
        self.inputs: np.ndarray | None = None
        self.processed: list = []
        self.core_points: list = []
        self.border_points: list = []
        self.noise_points: list = []
        self.clusters: list = []
        self.init_points: list = []

    def compute_eps_neighborhood(self, index: int) -> list:
        """
        eps neighborhood of p without p itself indices of points
        """
        neighbors = []
        p = self.inputs[index]
        for i, q in enumerate(self.inputs):
            if i == index:
                continue
            # euclidian distance
            d = np.sqrt(np.sum(np.square(p - q), axis=0))
            if d < self.eps:
                neighbors.append(i)
        return neighbors

    def form_new_cluster(self, p_ind, p_neighbors):
        new_cluster = {p_ind}

        def assign_neighbors(neighbors):
            for ind in neighbors:
                if ind in self.processed:
                    continue
                new_cluster.add(ind)
                self.processed.append(ind)
                n_neighbors = self.compute_eps_neighborhood(ind)
                if self.min_pts <= len(n_neighbors):
                    self.core_points.append(ind)
                    assign_neighbors(n_neighbors)
                else:
                    self.border_points.append(ind)
        assign_neighbors(p_neighbors)
        return list(new_cluster)

    def fit(self, inputs):
        self.inputs = inputs
        # 1) select an unprocessed point p
        for i, p in enumerate(self.inputs):
            if i in self.processed:
                continue

            self.processed.append(i)
            # 2) if p is not a core point, classify as noise and continue
            neighbors = self.compute_eps_neighborhood(i)
            # TODO should p be included in neighbors ?
            if self.min_pts <= len(neighbors):
                # 3) is core point, form new cluster
                self.core_points.append(i)
                print(f'forming new cluster from {self.inputs[i]}')
                self.init_points.append(self.inputs[i])
                self.clusters.append(self.form_new_cluster(i, neighbors))
            else:
                self.noise_points.append(i)


def main():
    X, _ = make_blobs(n_samples=64, centers=4, random_state=0x101)
    ds = DBSCAN(4, 1)
    ds.fit(X)
    for ind, p in enumerate(X):
        if ind in ds.core_points:
            pass
            #print(f'core point: {ind}, {p}')
        elif ind in ds.border_points:
            pass
            #print(f'border point: {ind}, {p}')
        elif ind in ds.noise_points:
            pass
            #print(f'noise point: {ind}, {p}')
        else:
            print(f'UNASSIGNED point: {ind}, {p}')

    plt.scatter(X[:, 0], X[:, 1], label='data')
    #for i, cluster in enumerate(ds.clusters):
        #plt.scatter(X[cluster][:, 0], X[cluster][:, 1], label=str(i))
    plt.scatter(X[ds.core_points][:, 0], X[ds.core_points][:, 1], label='core')
    plt.scatter(X[ds.border_points][:, 0], X[ds.border_points][:, 1], label='border')
    plt.scatter(X[ds.noise_points][:, 0], X[ds.noise_points][:, 1], label='noise')

    arr = np.array(ds.init_points)
    plt.scatter(arr[:, 0], arr[:, 1], c='black', marker='x', s=100, label='init')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    main()
