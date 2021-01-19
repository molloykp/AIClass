# Machine Learning
# PA1: Wine Data analysis

# Cameron Kelahan

import numpy as np
import math as math

trainData = np.load('wineTrainData.npy')
trainLabel = np.load('wineTrainLabel.npy')

class BinaryDT:

    dic = {}

    def __init__(self, X, y, maxDepth):

        self.globalNodeID = 0

        self.X = X
        self.y = y
        self.maxDepth = maxDepth
        self.rootNode = Node(X, y, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0)

        self.dic[self.globalNodeID] = self.rootNode

        def entropy(class0, class1):
            classTotal = class0 + class1

            if class0 > 0:
                class0Entropy = (class0 / classTotal) * math.log2(class0/classTotal)
            else:
                class0Entropy = 0
            if class1 > 0:

                class1Entropy = (class1 / classTotal) * math.log((class1/classTotal), 2)

            else:
                class1Entropy = 0

            entropyResult = -(class0Entropy + class1Entropy)

            if entropyResult == -0:
                entropyResult = 0

            if (entropyResult == -1):
                entropyResult = 1

            return entropyResult

        def splitPointGain(split_X, split_y, node):

            parentClass1 = sum(split_y)
            parentClass0 = split_y.size - parentClass1

            parentEntropy = entropy(parentClass0, parentClass1)

            # Set the current node's information to the following
            node.class0 = parentClass0
            node.class1 = parentClass1
            node.totalSamples = parentClass0 + parentClass1
            node.entropy = parentEntropy

            # Used in for loop to run through the columns of X
            attrRange = range(split_X[0].size)

            # Used to compare neighbors
            # Must be one less than max to avoid overflow when the end is reached
            compRange = range(split_y.size - 1)

            # Used to sort the values in X into <=0, >0, <=1, and >1 to
            # calculate entropy on and calculate infoGain
            sortRange = range(split_y.size)

            # The best infoGain found while running through the attributes of X
            maxInfoGain = 0

            # Attribute that produces the best infoGain
            bestAttr = 0

            # Splitpoint that produces the best entropy of the bestAttr
            splitPoint = 0

            # for loop to run through each column/attribute of X
            for attr in attrRange:

                # Creates an array of the values found in column 'attr'
                colOG = split_X[:,attr]

                # Creates a sorted version of the current column being inspected
                colSorted = np.copy(colOG)
                colSorted.sort()

                # for loop to run through each pair of neighbors in the current sorted column
                # Finds the breakpoint for each pair
                for index in compRange:

                    lesserValue = colSorted[index]
                    greaterValue = colSorted[index + 1]

                    # Makes sure the values that will be checked are not the same
                    # Needed for the entropy calculation later on
                    if (lesserValue != greaterValue):
                        breakPoint = (lesserValue + greaterValue) / 2

                        # Create variables to count how many 'lessEquals' there are in each class
                        # and how many 'greaters' there are in each class
                        # Used to calculate the entropy of the 'lessEquals' and the 'greaters'
                        leq0 = 0
                        leq1 = 0
                        greater0 = 0
                        greater1 = 0

                        # for loop to run through original column and calculate the entropy of the current breakpoint
                        # Remembers the best entropy and best breakpoint of the current column
                        for value in sortRange:

                            if colOG[value] <= breakPoint and split_y[value] == 0:
                                leq0 += 1
                            elif colOG[value] > breakPoint and split_y[value] == 0:
                                greater0 += 1
                            elif colOG[value] < breakPoint and split_y[value] == 1:
                                leq1 += 1
                            else:
                                greater1 += 1

                        totalNumValues = leq0 + leq1 + greater0 + greater1

                        # Calculates the weighted entropy of the values less than the breakPoint
                        # and the weighted entropy of the values greater than the breakpoint
                        weightedLessEqualsEntropy = entropy(leq0, leq1) * ((leq0 + leq1) / totalNumValues)
                        weightedGreaterEntropy = entropy(greater0, greater1) * ((greater0 + greater1) / totalNumValues)

                        totalChildEntropy = weightedLessEqualsEntropy + weightedGreaterEntropy

                        # Calculates the infoGain by subtracting the combination of the children entropy
                        # from the parent entropy
                        infoGain = parentEntropy - totalChildEntropy

                        # If the infoGain for this breakpoint in this attribute is greater than the previously
                        # recorded maxInfoGain, update the maxInfoGain to the current infoGain, the bestAttr
                        # to the current attr, and the splitPoint to the current splitPoint
                        if infoGain > maxInfoGain:
                            maxInfoGain = infoGain
                            bestAttr = attr
                            splitPoint = breakPoint

            return [bestAttr, splitPoint, maxInfoGain]

        def buildTree(node, depth):
            arrayOfSplits = splitPointGain(node.X, node.y, node)

            node.splitDim = arrayOfSplits[0]
            node.splitPoint = arrayOfSplits[1]
            node.infoGain = arrayOfSplits[2]

            if node.infoGain == 0 or depth == self.maxDepth:

                # counters for the two class types
                curClass0 = 0
                curClass1 = 0

                counterRange = range(node.y.size)

                for count in counterRange:
                    if node.y[count] == 0:
                        curClass0 += 1
                    else:
                        curClass1 += 1

                leafEntropy = entropy(curClass0, curClass1)

                node.entropy = leafEntropy
                node.splitDim = -1
                node.splitPoint = -1

            else:

                # Creates arrays to hold onto the values that are sorted
                leftChildX = []
                leftChildy = []
                rightChildX = []
                rightChildy = []

                counterRange = range(node.y.size)

                # Creates an array of the selected column that was deemed the best attribute to split on
                colOG = node.X[:, node.splitDim]

                # For each row, compare the value of the chosen attribute to the breakpoint, move the values of each row
                # to the left or right children respectively
                for count in counterRange:

                    if colOG[count] <= node.splitPoint:

                        leftChildy.append(node.y[count])
                        leftChildX.append(node.X[count])

                    else:

                        rightChildy.append(node.y[count])
                        rightChildX.append(node.X[count])

                leftChildNode = Node(np.array(leftChildX), np.array(leftChildy), self.globalNodeID + 1, depth + 1, -1, -1, -1,
                                0, 0, 0, 0, 0, 0)

                # increment the global node id variable since the previous number has been assigned
                # to the parent of this node
                self.globalNodeID += 1

                # Set the leftChildID of the current node to be that of the new left node
                node.leftNodeID = self.globalNodeID

                # Adding the new node, with the new node id, to the dictionary
                self.dic[self.globalNodeID] = leftChildNode

                rightChildNode = Node(np.array(rightChildX), np.array(rightChildy), self.globalNodeID + 1, depth + 1, -1, -1,
                              -1, 0, 0, 0, 0, 0, 0)
                self.globalNodeID += 1
                node.rightNodeID = self.globalNodeID
                self.dic[self.globalNodeID] = rightChildNode

                buildTree(leftChildNode, leftChildNode.depth)
                buildTree(rightChildNode, rightChildNode.depth)

        buildTree(self.rootNode, 0)

    def predict(self, n):

        def recursive(data, node):

            if node.leftNodeID == -1 or node.rightNodeID == -1:

                if node.class1 >= node.class0:

                    return [1, np.round(node.entropy, 3)]
                else:

                    return [0, np.round(node.entropy, 3)]
            else:

                val = data[node.splitDim]

                if val <= node.splitPoint:

                    return recursive(data, self.dic[node.leftNodeID])
                else:

                    return recursive(data, self.dic[node.rightNodeID])
        return recursive(n, self.rootNode)

    def print(self):

        def recursivePrint(node):
            if node.infoGain == 0 or node.infoGain == 1:
                node.infoGain = -1

                strInfoGain = "{0:.3f}".format(node.infoGain)
                strEntropy = "{0:.3f}".format(node.entropy)
                strSplit = "{0:.3f}".format(node.splitPoint)
                print("\t", node.nodeID, "\t", node.depth, "\t   ", node.leftNodeID, "\t\t", node.rightNodeID,
                      "\t   ", node.splitDim, "\t   ", strSplit, "\t", strEntropy, "   ", strInfoGain, "\t", node.class0,
                      "\t", node.class1, "\t", node.totalSamples)

                return
            else:

                strInfoGain = "{0:.3f}".format(node.infoGain)
                strEntropy = "{0:.3f}".format(node.entropy)
                strSplit = "{0:.3f}".format(node.splitPoint)
                print("\t", node.nodeID, "\t", node.depth, "\t   ", node.leftNodeID, "\t\t", node.rightNodeID,
                      "\t   ", node.splitDim, "\t   ", strSplit, "  \t", strEntropy, "   ", strInfoGain, "\t",
                      node.class0, "\t", node.class1, "\t", node.totalSamples)

                recursivePrint(self.dic[node.leftNodeID])
                recursivePrint(self.dic[node.rightNodeID])

                return

        print("nodeId\t   depth   leftNodeId\trightNodeId splitDim\tsplitPoint   entropy   infoGain   class0   class1   "
              "totalSamples")
        recursivePrint(self.rootNode)


class Node:
    def __init__(self, X, y, nodeID, depth, leftChildID, rightChildID, splitDim, splitPoint, entropy, infoGain, class0, class1,
                 totalSamples):
        self.X = X
        self.y = y
        self.nodeID = nodeID
        self.depth = depth
        self.leftNodeID = leftChildID
        self.rightNodeID = rightChildID
        self.splitDim = splitDim
        self.splitPoint = splitPoint
        self.entropy = entropy
        self.infoGain = infoGain
        self.class0 = class0
        self.class1 = class1
        self.totalSamples = totalSamples