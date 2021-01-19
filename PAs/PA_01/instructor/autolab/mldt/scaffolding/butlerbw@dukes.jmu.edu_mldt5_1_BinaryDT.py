import numpy as np
import math
import pandas as pd

"""
Binary decision tree.

author: Ben Butler
version: 9/25/19
"""


class BinaryDT:

    def __init__(self, X, y, maxDepth):
        """
        Preprocess data and build decision tree.

        :param X: An m by n numpy matrix that is organized by examples (rows) and features (columns)
        :param y: A length n numpy array that contains the class labels for each corresponding row in X
         (0 = false, 1 = true).
        :param maxDepth: The maximum depth of the decision tree
        """
        self.X = pd.DataFrame(data=X, index=y)  # create data frame with class labels
        self.max_depth = maxDepth

        self.dtree = {}
        self._build_tree(None, 0, self.X)
        if -1 in self.dtree.keys():
            del self.dtree[-1]  # remove empty key

    def _build_tree(self, parent_node, depth, data):
        """
        Build decision tree recursively.

        :param parent_node: the parent node of any new nodes created
        :param depth: the current depth of the tree
        :param data: the data to be split
        :return: None
        """
        # keep correct data for all nodes, yes this a weird way..
        if data is not None and not data.empty:
            self.X = self.X.drop(columns=[col for col in self.X.columns.tolist() if col not in data.columns.tolist()])
            data = data.drop(columns=[col for col in data.columns.tolist() if col not in self.X.columns.tolist()])

        # or data.index.unique == 1 or data.empty or (parent_node is not None and parent_node.splitDim == -1)
        if depth > self.max_depth or data is None or data.empty:  # reached max depth or class labels are the same
            parent_node.splitDim = -1
            # set class label
            if parent_node.class0 > parent_node.class1:
                parent_node.label = 0
            else:
                parent_node.label = 1

            self.dtree[parent_node.nodeId] = parent_node  # replace with updated leaf node
        else:
            node, left, right = self.find_best_split(parent_node, data)   # create node with best split feature

            self.dtree[node.nodeId] = node  # save node in tree with node id
            # save left and right node ids
            self.dtree[node.leftNodeId] = None
            self.dtree[node.rightNodeId] = None

            # print('node id: ', node.nodeId, 'depth: ', depth)
            # create left and right branches of node
            self._build_tree(parent_node=node, depth=depth+1, data=left)

            self._build_tree(parent_node=node, depth=depth+1, data=right)

    def predict(self, x):
        """
        Predict the class label given an array of values.
        :param x: numpy array of values
        :return: class label, node entropy
        """

        node = self.dtree[0]
        while True:
            if node.label is not None:
                break
            if x[node.splitDim] <= node.splitPoint:
                node = self.dtree[node.leftNodeId]
            else:
                node = self.dtree[node.rightNodeId]
        return node.label, node.entropy

    def print(self):
        """
        Print the tree values.
        :return: None
        """
        headers = ['nodeId', 'depth', 'leftNodeId', 'rightNodeId', 'splitDim', 'splitPoint', 'entropy', 'infoGain',
                   'class0', 'class1', 'totalSamples']
        for header in headers:
            end_with = ','
            if header == 'totalSamples':
                end_with = '\n'
            print(header, end=end_with)

        def _print(root_node: Node):
            print(root_node)
            if root_node is None: return
            # print(root_node.splitDim)
            if root_node.leftNodeId != -1:
                left_node = self.dtree[root_node.leftNodeId]
                _print(left_node)
            if root_node.rightNodeId != -1:
                right_node = self.dtree[root_node.rightNodeId]
                _print(right_node)

        node = self.dtree[0]
        _print(node)

    def find_best_split(self, parent_node, data):
        """
        Find the best data split and create a node from it.
        :param parent_node: parent node of the node to be created
        :param data: the data that will be split
        :return: child node, left data split, right data split
        """
        if parent_node is not None:
            depth = parent_node.depth + 1
            # set node id if left or right
            if self.dtree[parent_node.leftNodeId] is None:
                node_id = parent_node.leftNodeId
            else:
                node_id = parent_node.rightNodeId
        else:
            depth = 0
            node_id = 0

        is_empty = data.empty
        left_id = 2 * node_id + 1
        right_id = 2 * node_id + 2
        best_feature = None
        best_entropy = None
        best_split_point = None
        best_info_gain = 0.0
        best_left_split = None
        best_right_split = None
        class0 = 0
        class1 = 0

        # iterate over features to find best attribute to split on
        for feature in data.columns:
            data = data.sort_values(by=feature)  # sort continuous values of the feature
            values = data[feature].tolist()
            num_values = len(values)

            # parent entropy before split
            node_entropy = self.entropy(data[feature].index)
            # create split points and choose best info gain
            for value_index in range(num_values):
                split_point = 0.0
                value = values[value_index]
                # calculate mid point between values
                if value_index + 1 < num_values:
                    split_point = (value + values[value_index + 1]) / 2

                # split data on point
                left_split = data[data[feature] <= split_point]
                right_split = data[data[feature] > split_point]

                left_labels = left_split.index
                right_labels = right_split.index

                # left and right split entropy values
                l_entropy = self.entropy(left_labels)
                r_entropy = self.entropy(right_labels)
                total = num_values

                # weighted entropy
                weighted_entropy = (left_labels.size / total) * l_entropy + (right_labels.size / total) * r_entropy

                # set values from best info gain
                info_gain = node_entropy - weighted_entropy
                if best_info_gain <= info_gain:
                    best_feature = feature
                    best_entropy = node_entropy
                    best_split_point = split_point
                    best_info_gain = info_gain
                    best_left_split = left_split
                    best_right_split = right_split

        # make sure not to count values if data set is empty
        if not is_empty:
            class0 = np.count_nonzero(data[best_feature].index == 0)
            class1 = np.count_nonzero(data[best_feature].index)

        # is leaf node
        if best_info_gain == 0.0 or best_info_gain == 1.0:
            best_feature = -1.000
            best_split_point = -1.000
            best_info_gain = -1.000
            left_id = -1
            right_id = -1
        else:
            # remove best feature
            self.X = self.X.drop(columns=best_feature)
            best_left_split = best_left_split.drop(columns=best_feature)
            best_right_split = best_right_split.drop(columns=best_feature, axis=1)

        node = Node(
            node_id=node_id,
            depth=depth,
            l_node_id=left_id,
            r_node_id=right_id,
            split_dim=best_feature,
            split_point=best_split_point,
            entropy=best_entropy,
            info_gain=float(format(best_info_gain, '.3f')),
            class0=class0,
            class1=class1
        )

        # return node with left and right splits
        return node, best_left_split, best_right_split

    def entropy(self, values):
        """
        Calculate the entropy of a node with binary class labels.

        :param values: data frame, with values and class labels
        :return: the entropy of the values
        """
        if values.size == 0: return 0  # no values for the node
        # binary class labels..
        p0 = np.count_nonzero(values == 0) / values.size
        p1 = np.count_nonzero(values) / values.size
        if p0 == 0 or p1 == 0: return 0  # log2(0) does not work
        return -(p0 * math.log2(p0)) - (p1 * math.log2(p1))


class Node:
    def __init__(self, node_id, depth, l_node_id, r_node_id, split_dim, split_point, entropy, info_gain, class0, class1):
        self.nodeId = node_id
        self.depth = depth
        self.leftNodeId = l_node_id
        self.rightNodeId = r_node_id
        self.splitDim = split_dim
        self.splitPoint = split_point
        self.entropy = entropy
        self.infoGain = info_gain
        self.class0 = class0
        self.class1 = class1
        self.totalSamples = self.class0 + self.class1

        # label set if leaf node
        self.label = None

    def __str__(self):
        return f'{self.nodeId},{self.depth},{self.leftNodeId},{self.rightNodeId},{self.splitDim},' \
               f'{format(self.splitPoint, ".3f")},{format(self.entropy, ".3f")},{format(self.infoGain, ".3f")},' \
               f'{self.class0},{self.class1},{self.totalSamples}'

