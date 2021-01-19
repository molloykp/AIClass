from BinaryDT import *
from sklearn.datasets import load_wine
import sys

raw_data = load_wine()

#X = raw_data['data']
#y = raw_data['target']
XLabels = raw_data['feature_names']
'''
ind = np.where(y < 2)
ind2 = np.argsort(y)

Xsmall = X[ind[0],:]
ySmall = y[ind[0]]
'''

Xsmall = np.load(sys.argv[1])
ySmall = np.load(sys.argv[2])


testd = BinaryDT(Xsmall,ySmall, XLabels, 2)
testd.print()

#Xtest = np.load('wineTestData.npy')
#yTest = np.load('wineTestLabel.npy')

#print ('testing...')

#correct = 0
#for x,y in zip(Xtest,yTest):
#    yhat = testd.predict(x)
#    print (y, ' ', yhat)
#    if y == yhat[0]:
#        correct += 1
#print ('accuracy is:', (float)(correct)/len(yTest))
