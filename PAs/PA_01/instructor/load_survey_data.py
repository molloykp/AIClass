# https://www.kaggle.com/bsoyka3/have-you-ever/data
import numpy as np
import csv
from collections import Counter
import sklearn.model_selection

with open('data/responses.csv','r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    responses = []
    y = []
    classes = ['0-18', '19-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+']

    for row in reader:
        if (row.count('TRUE') + row.count('FALSE')) == 30:
            responses.append(row[2::])
            y.append(classes.index(row[1]))

# Convert boolean strings to 0/1
X = np.array(responses)
X = X == 'TRUE'
X = np.array(X, dtype=int)
print(X)

#combine everyone over 35
y = np.array(y)
y = np.minimum(y, 3)
print("Y", set(y))
# now pull 225 from each class
np.random.seed(42)
X_done=np.empty((0, X.shape[1]), dtype=int)
y_done= np.array([])
for cls in set(y):
    indices = y == cls
    y_cls = y[indices]
    X_cls = X[indices, :]
    indices = np.arange(y_cls.size)
    np.random.shuffle(indices)
    print(indices)
    y_cls = y_cls[indices[0:225]]
    X_cls = X_cls[indices[0:225]]
    X_done = np.append(X_done, X_cls, axis=0)
    y_done = np.append(y_done, y_cls)
    np.random.shuffle(indices)
    print(indices)
    #X_cls = X[indices,]

X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
    X_done, y_done, test_size=0.33333, random_state=42, stratify = y_done)

np.save('data/X_train.npy', X_train)
np.save('data/y_train.npy', y_train)
np.save('data/X_test.npy', X_test)
np.save('data/y_test.npy', y_test)
print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape, Counter(y_test))

from sklearn.tree import DecisionTreeClassifier
from decision_tree_mine import DecisionTree
from sklearn import metrics
tree = DecisionTree(max_depth=11)
tree.fit(X_train, y_train)
#print(tree.feature_importances_)
y_pred = tree.predict(X_test)
print(metrics.confusion_matrix(y_test, y_pred))
print(np.sum(y_pred == y_test)/ len(y_test))
#print(tree.score(X_test, y_test))

import sklearn.naive_bayes
nb = sklearn.naive_bayes.BernoulliNB()
nb.fit(X_train, y_train)
y_pred = nb.predict(X_test)
print(np.sum(y_pred == y_test)/ len(y_test))
print(metrics.confusion_matrix(y_test, y_pred))
