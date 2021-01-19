from BinaryDT import *
from sklearn.datasets import load_iris
import sys

raw_data = load_iris()

XLabels = raw_data['feature_names']


Xsmall = np.load('irisTrainData.npy')
ySmall = np.load('irisTrainLabel.npy')


testd = BinaryDT(Xsmall,ySmall, XLabels, 2)

Xtest = np.load('irisTestData.npy')
yTest = np.load('irisTestLabel.npy')
#yHat = np.zeros(shape=(yTest.shape[0], 2))

officialYHat  = np.load('irisTestLabelOfficialPredict.npy')

correct = 0
i = 0
officialMismatch = 0

verbose = True
for x,y in zip(Xtest,yTest):
    yhat = testd.predict(x)
    if len(yhat) != 2:
        print('predict should be returning a tuple (see the documentation)')
        sys.exit(99)

    #yHat[i] = yhat
    #print (y, ' ', yhat,officialYHat[i])
    if y == yhat[0]:
        correct += 1
    if officialYHat[i][0] != yhat[0] or officialYHat[i][1] != yhat[1]:
        officialMismatch += 1
        if verbose:
             print('mismatch on example ', i, ' in the test set.  Offcial tuple is:',
                  officialYHat[i], 'your answer is:',yhat)
    i += 1

if officialMismatch != 0:
    sys.exit(99)

#print(correct,len(yTest))
#np.save('irisTestLabelOfficialPredict',yHat)
