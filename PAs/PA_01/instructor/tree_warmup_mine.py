"""
Some warm-up coding for creating a Python decision tree.  Ultimately,
the impurity and gain methods should be moved into the decision_tree module,
and should probably be methods of the decision tree class.

Questions:
  What is the best split for the data below?
  What is the second best split?
"""

import numpy as np
import decision_tree


def impurity(y):
    """
    Calculate the Gini impurity of a collection of class labels.

    :param y: A numpy array of integer class labels.
    :return: A float between 0 and .5.
    """
    classes = set(y)
    probs = np.zeros(len(classes))
    for i, cur_class in enumerate(classes):
        probs[i] = np.count_nonzero(y == cur_class)
    probs /= y.size
    return -np.sum(probs * np.log2(probs))
    #return 1.0 - np.sum(probs ** 2)


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

        P_l = (float(split.y_left.size) /
              (split.y_left.size + split.y_right.size))
        P_r = 1.0 - P_l
        weighted_impurity = (P_l * impurity(split.y_left) +
                            P_r * impurity(split.y_right))

        print("left impurity: ", impurity(split.y_left))
        print("right impurity: ", impurity(split.y_right))
        print("weighted impurity: ", weighted_impurity)
        print("gain:", impurity(y) - weighted_impurity)
        print()

if __name__ == "__main__":
    split_demo()
