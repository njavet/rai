from sklearn import datasets



class Node:
    def __init__(self):
        self.gini: float
        self.samples: int 
        self.value: list
        self.class_: str
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def gini_impurity(self):
        ps = []
        for v in self.value:
            ps.append((1 / self.samples) * v)
        self.gini = 1 - functools.reduce(operator.add, [pi**2 for pi in ps])




def main():
    iris = datasets.load_iris()
    X = iris.data[0:, 2:4]
    y = iris.target

    n_unique = np.unique(X[:, 0])
    thresholds = list(map(lambda pair: (pair[0] + pair[1]) / 2,
                          zip(n_unique, n_unique[1:])))
    
    splits = {}
    for ti in thresholds:
        x_left = np.where(X[:, 0] <= ti)
        x_right = np.where(ti < X[:, 0])






if __name__ == '__main__':
    main()

