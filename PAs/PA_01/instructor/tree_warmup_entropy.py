"""
Some warm-up coding for creating a Python decision tree.  Ultimately,
the impurity method and gain calculations should be moved into the
decision_tree module, and should probably be methods of the decision tree class.

Questions:
  What is the best split for the data below?
  What is the second best split?
"""

import numpy as np
import decision_tree_mine_fast as decision_tree


def impurity(y):
    """
    Calculate the entropy impurity of a collection of class labels.

    :param y: A numpy array of integer class labels.
    :return: A float that represents the computed entropy.
    """
    pass


def split_demo():
    X = np.array([[1., 0., 120.],
                  [0., 1., 100.],
                  [1., 0., 70.],
                  [0., 0., 150.],
                  [1., 2., 85.],
                  [0., 1., 80.],
                  [0., 0., 75.]])

    y = np.array([0, 0, 0, 1, 0, 1, 1])
    for split in decision_tree.split_generator(X, y):
        print(split)

        # NOW CALCULATE AND PRINT THE WEIGHTED IMPURITY
        # AND THE GAIN.

        print()

if __name__ == "__main__":
    split_demo()
