import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn import svm

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline


class MaximalMarginClassifier:
    def __init__(self, random_seed=0x101):
        self.rng = np.random.default_rng(random_seed)
        self.intercept_ = None
        self.weights_ = None

    def _init_weights(self, n):
        self.intercept_ = self.rng.standard_normal()
        self.weights_ = self.rng.standard_normal(n)

    def fit(self, X, y):
        self._init_weights(X.shape[1])

    def predict(self, x):
        return self.intercept_ + np.dot(self.weights_, x)


def visualize_svm():
    cmap = mpl.colors.ListedColormap(['red', 'black', 'blue'])
    X, y = datasets.make_blobs(n_samples=101,
                               centers=2,
                               random_state=0x101,
                               cluster_std=0.6)
    y[np.where(y == 0)] = -1
    fig, ax = plt.subplots(figsize=(5, 5))
    plt.grid(color='gray', linestyle='-')
    ax.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap=cmap, label='Data points')
    ax.set_xlabel(r'$x_1$', fontsize=16)
    ax.set_ylabel(r'$x_2$', fontsize=16)

    model = svm.SVC(kernel='linear', C=1000, tol=0.0001)
    model.fit(X, y)
    w = model.coef_[0]
    b = model.intercept_[0]

    ax.scatter(w[0], w[1], c='orange')
    ax.scatter(model.support_vectors_[:, 0],
               model.support_vectors_[:, 1],
               c='green', label='Support Vectors')

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    #xx = np.linspace(x_min, x_max)
    weights = model.coef_[0]
    slope = -weights[0] / weights[1]
    idb = -model.intercept_ / weights[1]
    decb = np.array([idb[0], slope])
    print('weights', weights)
    print('decb', decb)
    print(np.dot(w, decb))

    #ax.plot(xx, [(-b/w[1]) + (-w[0]/w[1])*xi for xi in xx])


    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                         np.arange(y_min, y_max, 0.01))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')

    margin = 1 / np.linalg.norm(weights)
    gutter_up = idb + margin
    gutter_down = idb - margin

    # Reshape the predictions to match the shape of the mesh grid

    # Plot the mesh grid with colors corresponding to the predicted class labels
    x_plot = np.linspace(x_min, x_max, 100)
    y_plot = slope * x_plot + idb
    ax.plot(x_plot, y_plot, c='cyan')
    ax.plot(x_plot, y_plot + margin, c='black')
    ax.plot(x_plot, y_plot - margin, c='black')
    #ax.fill_between(x_plot, y_plot, y_plot + margin, color='blue', alpha=0.1)
    #ax.fill_between(x_plot, y_plot, y_plot - margin, color='red', alpha=0.1)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    visualize_svm()





