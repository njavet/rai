
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.svm import SVC

X, y = make_blobs(n_samples=16,
                  random_state=0x101)

clf = SVC()
clf.fit(X, y)
svs = clf.support_vectors_

plt.scatter(X[:, 0], X[:, 1])
plt.scatter(svs[:, 0], svs[:, 1])
plt.show()
