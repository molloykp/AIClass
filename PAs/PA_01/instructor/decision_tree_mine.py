"""Pure Python Decision Tree Classifier.

Simple binary decision tree classifier.  Splits are based on Gini impurity.

Author: Nathan Sprague and ???
Version:

"""
import numpy as np
from collections import namedtuple

# Named tuple is a quick way to create a simple wrapper class...
Split_ = namedtuple('Split',
                    ['dim', 'pos', 'X_left', 'y_left', 'X_right', 'y_right'])


class Split(Split_):
    """
    Represents a possible split point during the decision tree creation process.

    Attributes:

        dim (int): the dimension along which to split
        pos (float): the position of the split
        X_left (ndarray): all X entries that are <= to the split position
        y_left (ndarray): labels corresponding to X_left
        X_right (ndarray):  all X entries that are > the split position
        y_right (ndarray): labels corresponding to X_right
    """
    pass


def split_generator(X, y):
    """
    Utility method for generating all possible splits of a data set
    for the decision tree construction algorithm.

    :param X: Numpy array with shape (num_samples, num_features)
    :param y: Numpy integer array with length num_samples
    :return: A generator for Split objects that will yield all
            possible splits of the data
    """

    # Loop over all of the dimensions.
    for dim in range(X.shape[1]):
        # Get the indices in sorted order so we can sort both  data and labels
        ind = np.argsort(X[:, dim])

        # Copy the data and the labels in sorted order
        X_sort = X[ind, :]
        y_sort = y[ind]

        # Loop through the midpoints between each point in the current dimension
        for index in range(1, X_sort.shape[0]):

            # don't try to split between equal points.
            if X_sort[index - 1, dim] != X_sort[index, dim]:
                pos = (X_sort[index - 1, dim] + X_sort[index, dim]) / 2.0

                # Yield a possible split.  Note that the slicing here does
                # not make a copy, so this should be relatively fast.
                yield Split(dim, pos,
                            X_sort[0:index, :], y_sort[0:index],
                            X_sort[index::, :], y_sort[index::])



class DecisionTree:
    """
    A binary decision tree classifier for use with real-valued attributes.

    Attributes:
        classes (set) - The set of classes this tree can classify.
    """

    def __init__(self, max_depth=np.inf):
        """
        Decision tree constructor.

        :param max_depth: limit on the tree depth.
                          A depth 0 tree will have no splits.
        """
        self.max_depth = max_depth
        self.classes = {}
        self.depth = 0
        self._root = None
        self.tie = False

    def fit(self, X, y):
        """
        Construct the decision tree using the provided data and labels.

        :param X: Numpy array with shape (num_samples, num_features)
        :param y: Numpy integer array with length num_samples
        """
        self.classes = set(y)
        self._root = Node(X, y)
        self._build(self._root, 0)

    def check_for_tie(self, node):
        goodnesses = []
        for split in split_generator(node.X, node.y):
            goodnesses += [self.goodness(node, split.y_left, split.y_right)]
        goodnesses.sort()
        print(goodnesses)
        return np.isclose(goodnesses[-1], goodnesses[-2])

    def _build(self, node, depth):

        if depth > self.depth:
            self.depth = depth

        if self.impurity(node.y) > 0 and depth < self.max_depth:
            best_split = None
            best_goodness = -1.0
            self.tie = self.tie or self.check_for_tie(node)
            for split in split_generator(node.X, node.y):

                goodness = self.goodness(node, split.y_left, split.y_right)
                if goodness > best_goodness:
                    best_goodness = goodness
                    best_split = split
            if best_split is not None:
                node.left = self._build(Node(best_split.X_left,
                                             best_split.y_left), depth + 1)
                node.right = self._build(Node(best_split.X_right,
                                              best_split.y_right), depth + 1)
                node.split = best_split

        return node

    def impurity(self, y):
        probs = np.zeros(len(self.classes))
        for i, cur_class in enumerate(self.classes):
            probs[i] = np.count_nonzero(y == cur_class)
        probs /= y.size
        return 1.0 - np.sum(probs ** 2)
        # return -np.sum(np.nan_to_num(probs * np.log2(probs)))

    def goodness(self, node, y_left, y_right):
        """ Goodness of split"""
        P_l = float(y_left.size) / (y_left.size + y_right.size)
        P_r = 1.0 - P_l
        return self.impurity(node.y) - P_l * self.impurity(
            y_left) - P_r * self.impurity(y_right)

    def predict(self, X):
        """
        Predict labels for a data set by finding the appropriate leaf node for
        each input and using the majority label as the prediction.

        :param X:  Numpy array with shape (num_samples, num_features)
        :return: A length num_samples numpy array containing predicted labels.
        """
        y = np.empty(X.shape[0], dtype=int)
        for i in range(y.size):
            y[i] = self._root.predict(X[i, :])
        return y

    def get_depth(self):
        """
        :return: The depth of the decision tree.
        """
        return self.depth


class Node:
    """
    It will probably be useful to have a Node class.  In order to use the
    visualization code in draw_trees, the node class must have three
    attributes:

    Attributes:
        left:  A Node object or Null for leaves.
        right - A Node object or Null for leaves.
        split - A Split object representing the split at this node,
                or Null for leaves
    """
    next_id = 0

    def __init__(self, X, y, split=None):
        self.X = X
        self.y = y
        self.classes = set(y)
        self.left = None
        self.right = None
        self.split = split
        self.id = Node.next_id
        Node.next_id += 1

    def predict(self, x):
        if self.is_leaf():
            best_class = None
            top_count = -1
            for cls in self.classes:
                count = np.count_nonzero(self.y == cls)
                if count > top_count:
                    top_count = count
                    best_class = cls
            return best_class
        else:
            if x[self.split.dim] <= self.split.pos:
                return self.left.predict(x)
            else:
                return self.right.predict(x)

    def is_leaf(self):
        return self.left is None

    def size(self):
        return self.y.size

    def __repr__(self):
        return "NODE:\n" + self.X.__repr__() + "\n"

def tree_demo():
    import draw_tree
    X = np.array([[0.88, 0.39],
                  [0.49, 0.52],
                  [0.68, 0.26],
                  [0.57, 0.51],
                  [0.61, 0.73]])
    y = np.array([1, 0, 0, 0, 1])
    tree = DecisionTree()
    tree.fit(X, y)
    draw_tree.draw_tree(X, y, tree)

if __name__ == "__main__":
    tree_demo()
    import draw_tree
    import matplotlib.pyplot as plt
    from sklearn.tree import DecisionTreeClassifier

    # tree = DecisionTreeClassifier(random_state=0)
    done = False
    while True:
        while not done:
            num = 10
            X = np.around(np.random.random((num, 2)), decimals=2)
            print(X)
            # y = np.zeros((num,))
            # y[(X[:,0] + X[:,1] > 1.5) | (X[:,0] + X[:,1] < .5)] = 1
            y = np.random.randint(2, size=(num,))
            tree = DecisionTree(max_depth=1)
            tree.fit(X, y)
            print(tree.depth)
            print(tree.tie)
            done = not tree.tie and tree.depth >=1

        # X_test = np.random.random((20, 2)) * 1000 - 100
        # print(X_test)
        # print(tree.predict(X_test))
        print(repr(X))
        print(repr(y))
        plt.figure(figsize=(3.5, 3))
        draw_tree.draw_tree(X, y, tree)
        plt.gcf().savefig('tmp.pdf',dpi=400,bbox_inches='tight',pad_inches=0.05)
        plt.show()
        done = False
