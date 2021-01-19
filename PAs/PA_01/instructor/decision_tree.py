"""Pure Python Decision Tree Classifier.

Simple multi-class binary decision tree classifier.
Splits are based on entropy impurity.

Initial Author: Nathan Sprague
Modified by:
 molloykp -- added comments and switch impurity to entropy

"""

import numpy as np
from collections import namedtuple
import argparse
import math
import matplotlib.pyplot as plt

# Named tuple is a quick way to create a simple wrapper class...
Split_ = namedtuple('Split',
                    ['dim', 'pos', 'X_left', 'y_left', 'X_right', 'y_right'])


# This class does not require any student modification
# treat it as an immutable object without any methods
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

def impurity(classes, y):
    """
    Return the impurity/entropy of the data in y

    :param classes: list of the classes
                 y: Numpy array with class labels having shape (num_samples_in_node,)

    :return: A scalar with the entropy of the class labels
    """
    """ Entropy impurity for class labels y """

    entropy = 0
    for i, cur_class in enumerate(classes):
        class_freq = np.count_nonzero(y == cur_class)
        if class_freq != 0:
            entropy += class_freq/y.size * math.log(class_freq/y.size, 2)


    return entropy * -1

def weighted_impurity(classes, y_left, y_right):
    """
    Weighted entropy impurity for a possible split.
    :param classes: list of the classes
             y_left: class labels for the left node in the split
             y_right: class labels for the right node in the spit

    :return: A scalar with the weighted entropy

    """

    P_l = y_left.size / (y_left.size + y_right.size)
    P_r = 1.0 - P_l

    return P_l * impurity(classes, y_left) + P_r * impurity(classes, y_right)


class DecisionTree:
    """
    A binary decision tree classifier for use with real-valued attributes.

    Attributes:
        classes (set): The set of integer classes this tree can classify.
    """

    def __init__(self, max_depth=np.inf):
        """
        Decision tree constructor.

        :param max_depth: limit on the tree depth.
                          A depth 0 tree will have no splits.
        """

        self.max_depth = max_depth
        self.depth = 0
        self.classes = {}
        self._root = None

        # Dictionary used to keep track of total weighted gain
        # for each split dimension:
        self.feature_importances = dict()


    def fit(self, X, y):
        """
        Construct the decision tree using the provided data and labels.

        :param X: Numpy array with shape (num_samples, num_features)
        :param y: Numpy integer array with length num_samples
        """

        self.classes = set(y)
        self._root = self._build(X, y, 0)


    def _build(self, X, y, depth):
        """ Helper method for depth-first recursive tree construction.

        """

        # Cache the tree depth so we don't need to recalculate it
        # for the get_depth method.
        if depth > self.depth:
            self.depth = depth

        node = Node(X, y)

        node_impurity = impurity(self.classes, y)

        if node_impurity > 0 and depth < self.max_depth:
            best_split = None
            best_gain = -1.0
            for split in split_generator(X, y):
                gain = node_impurity - weighted_impurity(self.classes,split.y_left,
                                                               split.y_right)
                if gain > best_gain:
                    best_gain = gain
                    best_split = split

            if best_split is not None: # possible for identical points
                node.left = self._build(best_split.X_left,
                                        best_split.y_left, depth + 1)
                node.right = self._build(best_split.X_right,
                                         best_split.y_right, depth + 1)
                node.split = best_split

                # Track feature importances for analysis
                importance = best_gain * node.y.size
                if best_split.dim not in self.feature_importances:
                    self.feature_importances[best_split.dim] = importance
                else:
                    self.feature_importances[best_split.dim] += importance

        return node

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
        self.left = None
        self.right = None
        self.split = split
        self.id = Node.next_id
        Node.next_id += 1


    def predict(self,x):
        """
        Recurisively find the appropriate leaf and return the class label
        for a single point.

        """
        if self.is_leaf():
            labels, counts = np.unique(self.y, return_counts=True)
            return labels[np.argmax(counts)]
        else:
            if x[self.split.dim] < self.split.pos:
                return self.left.predict(x)
            else:
                return self.right.predict(x)

    def is_leaf(self):
        """ True if this node is a leaf."""
        return self.left is None

    def size(self):
        """ Return the number of points stored in this leaf. """
        return self.y.size

    def print_tree(self, depth):
        """Recursive method to print the entire subtree rooted at this
        node.

        """
        print("    " * depth, end='')
        print(repr(self))
        if not self.is_leaf():
            self.left.print_tree(depth + 1)
            self.right.print_tree(depth + 1)

    def __repr__(self):
        """ String representation of this node. """
        if not self.is_leaf():
            return "NODE: split dim: {} split point: {}".format(self.split.dim,
                                                                self.split.pos)
        else:
            return "LEAF: {}".format(self.predict(None))



def tree_demo(parms):
    import draw_tree

    X = np.array([[0.88, 0.39],
                  [0.49, 0.52],
                  [0.68, 0.26],
                  [0.57, 0.51],
                  [0.61, 0.73]])
    y = np.array([1, 0, 0, 0, 1])


    tree = DecisionTree(max_depth=parms.depth_limit)

    tree.fit(X, y)

    draw_tree.draw_tree(X, y, tree)

    plt.show()

def parse_args():
    parser = argparse.ArgumentParser(description='Decision Tree modeling')

    parser.add_argument('--inputTrainX', action='store',
                        dest='trainx_filename', default="", required=False,
                        help='numpy npy file for the training X matrix')

    parser.add_argument('--inputTrainy', action='store',
                        dest='trainy_filename', default="", required=False,
                        help='numpy npy file for the training labels (y vector)')

    parser.add_argument('--inputTestX', action='store',
                        dest='testx_filename', default="", required=False,
                        help='numpy npy file for the testing X matrix')

    parser.add_argument('--inputTesty', action='store',
                        dest='testy_filename', default="", required=False,
                        help='numpy npy file for the testing labels (y vector)')

    parser.add_argument('--depthLimit', action='store', type=int,
                        dest='depth_limit', default=np.inf, required=False,
                        help='max depth of the decision tree')

    parser.add_argument('--testDataFile', action='store',
                        dest='test_data_filename', default="", required=False,
                        help='data file with test data')

    parser.add_argument('--treeModelFile', action='store',
                        dest='tree_model_file', default="", required=False,
                        help='output of the learned model/tree')

    parser.add_argument('-demoFlag', '--demoFlag',action='store_true',
                        dest='demo_flag',
                        help='run demo data hardcoded into program')

    return parser.parse_args()


def main():
    parms = parse_args()

    if parms.demo_flag:
       tree_demo(parms)
    else:
        # read in training and test data
        # compute model on training data
        # run test data
        # optionally print out tree model
        X_train = np.load(parms.trainx_filename)
        y_train  = np.load(parms.trainy_filename)

        X_test  = np.load(parms.testx_filename)
        y_test = np.load(parms.testy_filename)

        # check dimensions
        assert(X_train.shape[0] == y_train.shape[0])
        assert(X_test.shape[0] == y_test.shape[0])
        assert(X_train.shape[1] == X_test.shape[1])

        tree = DecisionTree(max_depth=parms.depth_limit)
        tree.fit(X_train, y_train)

        yhat = tree.predict(X_test)

        acc = np.count_nonzero(y_test == yhat)/y_test.size
        print('Accuracy: {:0.4f}'.format(acc))

if __name__ == "__main__":
    main()
