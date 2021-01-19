import numpy as np
from decision_tree_mine_fast import DecisionTree

a = np.loadtxt('wifi_localization.txt', delimiter='\t')
np.random.seed(0)
np.random.shuffle(a)
X = a[:, 0:-1]
y = a[:,-1]
num = X.shape[0]
split_pnt = int(num * .8)
X_train = X[0:split_pnt,:]
y_train = y[0:split_pnt]
X_test = X[split_pnt::,:]
y_test = y[split_pnt::]

X_train = np.load('x_train.npy')[:, ::32]
X_test = np.load('x_test.npy')[:, ::32]
y_train = np.load('y_train.npy')
y_test = np.load('y_test.npy')
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)
tree = DecisionTree(8)
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import sklearn
print(sklearn.__version__)
#tree = RandomForestClassifier(random_state=0)
tree = DecisionTreeClassifier(max_depth=8, random_state=0)
tree.fit(X_train, y_train)
y_pred = tree.predict(X_test)

print(np.sum(y_pred == y_test)/y_pred.size)
print(tree.get_depth())

#print(a)