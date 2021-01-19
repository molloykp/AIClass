"""
Submission tests for Machine Learning Decision Tree Project

Author: Nathan Sprague
Version: 2/6/2020
"""

import unittest
import numpy as np
import time
import sklearn.datasets
from decision_tree import DecisionTree, impurity, weighted_impurity
from decision_tree_tests import *

from unittest_utils import points_decor
import sys

class MyHiddenTestCases(unittest.TestCase):
    def setUp(self):
        # These data sets are carefully selected so that there should be
        # no ties during tree construction.  This means that there should
        # be a unique correct tree for each.

        self.X2 = np.array([[0.88, 0.39],
                            [0.49, 0.52],
                            [0.68, 0.26],
                            [0.57, 0.51],
                            [0.61, 0.73]])
        self.y2 = np.array([1, 0, 0, 0, 1])

    @points_decor(points=10, autograder_name='HiddenTests')
    def test_this_runs(self):
        tree = DecisionTree(max_depth=0)
        tree.fit(self.X2, self.y2)
        X_test = np.random.random((100, 2)) - .5 * 2
        y_test = tree.predict(X_test)
        self.assertTrue(np.alltrue(y_test == 0))

if __name__ == '__main__':
    try:
        unittest.main(exit=False)
    except:
        print('in except from main')

    points_decor.print_json()

    points = points_decor.return_points()

    sys.exit(points)
