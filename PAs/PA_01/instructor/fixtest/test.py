from decision_tree_done import DecisionTree
from decision_tree import DecisionTree as DecisionTreeO
import numpy as np
import matplotlib.pyplot as plt

x_train = np.load('X_train.npy')
y_train = np.load('y_train.npy')
x_test  = np.load('X_test.npy')
y_test  = np.load('y_test.npy')

tree = DecisionTree(max_depth=5)
tree.fit(x_train, y_train)

tree1 = DecisionTreeO(max_depth=5)
tree1.fit(x_train, y_train)

tree._root.print_tree(0)
#tree1._root.print_tree(0)
