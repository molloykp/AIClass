from BinaryDT import *
import sys


if len(sys.argv) != 7:
    print('Incorrect number of arguments, expecting 7 supplied',len(sys.argv))
    sys.exit(99)

Xsmall = np.load(sys.argv[1])
ySmall = np.load(sys.argv[2])

depth = (int)(sys.argv[3])

Xtest = np.load(sys.argv[4])
yTest = np.load(sys.argv[5])

officialYHat  = np.load(sys.argv[6])

testd = BinaryDT(Xsmall,ySmall, depth)

correct = 0
i = 0
officialMismatch = 0

verbose = True
for x,y in zip(Xtest,yTest):
    yhat = testd.predict(x)
    if len(yhat) != 2:
        print('predict should be returning a tuple (see the PA instructions)')
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

#np.save('wineTestLabelOfficialPredict',yHat)
#if correct != len()
