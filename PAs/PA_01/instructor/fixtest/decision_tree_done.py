"""Pure Python Decision Tree Classifier.

Simple binary decision tree classifier.  Splits are based on Gini impurity.

Author: Nathan Sprague and ???
Version:

"""
import numpy as np
from collections import namedtuple, Counter

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

    def fit(self, X, y):
        """
        Construct the decision tree using the provided data and labels.

        :param X: Numpy array with shape (num_samples, num_features)
        :param y: Numpy integer array with length num_samples
        """
        self.classes = set(y)
        self._root = self._build(X, y, 0)


    def _build(self, X, y, depth):

        if depth > self.depth:
            self.depth = depth

        node = Node(X, y)
        
        if self.impurity(y) > 0 and depth < self.max_depth:
            best_split = None
            best_gain = -1.0
            for split in split_generator(X, y):
                gain = self.gain(y, split.y_left, split.y_right)
                if gain > best_gain:
                    best_gain = gain
                    best_split = split
                    
            if best_split is not None: # possible for identical points
                node.left = self._build(best_split.X_left,
                                        best_split.y_left, depth + 1)
                node.right = self._build(best_split.X_right,
                                         best_split.y_right, depth + 1)
                node.split = best_split

        return node

    def impurity(self, y):
        probs = np.zeros(len(self.classes))
        for i, cur_class in enumerate(self.classes):
            probs[i] = np.count_nonzero(y == cur_class)
        probs /= y.size
        return 1.0 - np.sum(probs ** 2)
        # return -np.sum(np.nan_to_num(probs * np.log2(probs)))

    def gain(self, y_parent, y_left, y_right):
        """ Gain of split"""
        P_l = y_left.size / y_parent.size
        P_r = 1.0 - P_l
        return self.impurity(y_parent) - P_l * self.impurity(
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

    def print_tree(self):
        self._root.print_tree(0)


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
        self.left = None
        self.right = None
        self.split = split
        self.id = Node.next_id
        Node.next_id += 1

    def predict(self, x):
        if self.is_leaf():
            labels, counts = np.unique(self.y, return_counts=True)
            return labels[np.argmax(counts)]
        else:
            if x[self.split.dim] < self.split.pos:
                return self.left.predict(x)
            else:
                return self.right.predict(x)

    def is_leaf(self):
        return self.left is None

    def size(self):
        return self.y.size

    def print_tree(self, depth):
        print("    " * depth, end='')
        print(repr(self))
        if not self.is_leaf():
            self.left.print_tree(depth + 1)
            self.right.print_tree(depth + 1)
    
    def __repr__(self):
        if not self.is_leaf():
            return "NODE: split dim: {} split point: {}".format(self.split.dim,
                                                                self.split.pos)
        else:
            return "LEAF: {}".format(self.predict(None))
