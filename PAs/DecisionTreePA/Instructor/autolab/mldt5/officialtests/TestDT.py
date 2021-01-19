#    Name: TestDT.py
#  Author: molloykp
#    Date: Sept 2019
# Purpose: Compare two decision trees and report if they are equal.
#              
#          Each node of the tree is imported into a dictionary by 
#          nodeId. Then, an inorder traversal is performed 
#          and the data fields are compared (excludes nodeIds).  
#
# Returns: 0 if trees match 
#          1 if trees DO NOT match
# 
#    Args: filename to the baseline tree
#          filename to the submission tree

from BinaryDT import *
import csv
import sys


# read a file that represents a decision tree
# storing the column name as the key in a dictionary
def buildADictionary(fileName):
    csv.register_dialect('MyDialect', quotechar='"', skipinitialspace=True, quoting=csv.QUOTE_NONE, lineterminator='\n', strict=True)
    decisionTree = csv.DictReader(open(fileName),dialect='MyDialect')
    decisionDict = {}
    for node in decisionTree:
        decisionDict[node['nodeId']] = node

    return decisionDict

# 
def testTree(baselineTree,studentTree):
    errorDetected = False
    treeLevel = 0
    nodeId = '0' # start at the root
    errorDetected = _testTree(baselineTree,nodeId,studentTree,nodeId, treeLevel,
                              errorDetected)
    return errorDetected

def _testTree(baselineTree,bNodeId,studentTree,sNodeId, level, errorDetected):
    fieldsToCompare = ['splitDim', 'splitPoint', 'entropy', 'infoGain', 'class0', 'class1', 'totalSamples']
    if level > 6:
        print('recursive tree depth exceeded 7, terminating')
        return True

    baseNode = baselineTree.get(bNodeId)
    compareNode = studentTree.get(sNodeId)

    if baseNode == None:
        print('key error in solution, missing value is:',bNodeId, ' level:',level)
        return True
    if compareNode == None:
        print('key error in student solution, missing value is:', sNodeId, ' level:', level)
        return True

    # compare the fields
    for f in fieldsToCompare:
        #if baseNode[f] != compareNode[f]:
        if abs(float(baseNode[f]) - float(compareNode[f])) > 0.001:
            print('depth:', level, ' node id: ',sNodeId, ' ', f,' expected:', baseNode[f], ' actual:', compareNode[f])
            errorDetected = True
    # if both agree there is a child, go
    if baseNode['leftNodeId'] != '-1' and compareNode['leftNodeId'] != '-1':
        errorDetected = _testTree(baselineTree,baseNode['leftNodeId'],
                                  studentTree,compareNode['leftNodeId'], 
                                  level + 1,errorDetected)
        if baseNode['rightNodeId'] != '-1' and compareNode['rightNodeId'] != '-1':
            errorDetected = _testTree(baselineTree,baseNode['rightNodeId'],
                                      studentTree,compareNode['rightNodeId'],
                                      level + 1, errorDetected)
        else:
            print('left child detected, right child missing')
            errorDetected = True
    elif baseNode['leftNodeId'] == '-1' and compareNode['leftNodeId'] != '-1':
        print('Node id:',sNodeId, ' had an unexpected left childNode')
        errorDetected = True
    elif compareNode['leftNodeId'] == '-1' and baseNode['leftNodeId'] != '-1':
        print('Node id:', sNodeId, ' missing an expected left childNode')
        errorDetected = True

    return errorDetected


# main

d1 = buildADictionary(sys.argv[1])
d2 = buildADictionary(sys.argv[2])


errorDetected = testTree(d1, d2)

if errorDetected == True:
    sys.exit(1)
else:
    sys.exit(0)
