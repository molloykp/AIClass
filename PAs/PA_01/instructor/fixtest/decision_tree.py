"""Pure Python Decision Tree Classifier.

Simple multi-class binary decision tree classifier.
Splits are based on Gini impurity.

Author: Nathan Sprague and Shady Abdalla
Version: 1

"""
import numpy as np
from collections import namedtuple

from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
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
        classes (set): The set of integer classes this tree can classify.
    """
    classes = {}
    _root = None
    max_depth = 0
    depth = 0

    def __init__(self, max_depth=np.inf):
        """
        Decision tree constructor.

        :param max_depth: limit on the tree depth.
                          A depth 0 tree will have no splits.
        """
        self.max_depth = max_depth

    def impurity(self, y):
        ratio = []
        for e in self.classes:
            ratio.append(np.square(np.count_nonzero(y == e) / len(y)))
        return 1 - sum(ratio)

    def best_split(self, X, y):
        gini_parent = self.impurity(y)
        highest_gain = 0
        best_split = None
        for split in split_generator(X, y):
            weight_gini = (split.y_right.shape[0] / X.shape[0]) * self.impurity(split.y_right) + \
                          (split.y_left.shape[0] / X.shape[0]) * self.impurity(split.y_left)
            gain = gini_parent - weight_gini
            if gain > highest_gain:
                best_split = split
                highest_gain = gain
        return best_split

    def fit(self, X, y):
        """
        Construct the decision tree using the provided data and labels.

        :param X: Numpy array with shape (num_samples, num_features)
        :param y: Numpy integer array with length num_samples
        """
        self.classes = set(y)
        self._root = self.grow_tree(X, y)

    def grow_tree(self, X, y, depth=0):
        node = Node()
        split = self.best_split(X, y)
        node.split = split

        n_r, counts = np.unique(y, return_counts=True)

        node.predicted_class = n_r[np.argmax(counts)]
        if split is None:
            return node
        if depth < self.max_depth:
            node.left = self.grow_tree(split.X_left, split.y_left, depth + 1)
            node.right = self.grow_tree(split.X_right, split.y_right, depth + 1)
            self.depth += 1
        return node

    def predict(self, X):
        """
        Predict labels for a data set by finding the appropriate leaf node for
        each input and using the majority label as the prediction.

        :param X:  Numpy array with shape (num_samples, num_features)
        :return: A length num_samples numpy array containing predicted labels.
        """
        if self.max_depth == 0:
            return self._root.predicted_class
        return [self.predict_util(sample) for sample in X]

    def predict_util(self, sample):
        node = self._root

        while node.left:
            if sample[node.split.dim] < node.split.pos:
                node = node.left
            else:
                node = node.right
        return node.predicted_class

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
    left = None
    right = None
    split = None
    predicted_class = None

    def __init__(self, left=None, right=None, split=None, predicted_class=None):
        self.left = left
        self.right = right
        self.split = split
        self.predicted_class = predicted_class

    def print_tree(self, depth):
        print("    " * depth, end='')
        print(repr(self))
        if not self.left is None:
            self.left.print_tree(depth + 1)
            self.right.print_tree(depth + 1)
    
    def __repr__(self):
        if not self.left is None:
            return "NODE: split dim: {} split point: {}".format(self.split.dim,
                                                                self.split.pos)
        else:
            return "LEAF: {}".format(self.predicted_class)
