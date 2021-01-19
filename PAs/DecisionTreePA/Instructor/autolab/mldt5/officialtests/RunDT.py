from BinaryDT import *
import sys


Xsmall = np.load(sys.argv[1]) # load training data
ySmall = np.load(sys.argv[2]) # load test data

depth = (int) (sys.argv[3]) # tree depth

testd = BinaryDT(Xsmall,ySmall, depth)
testd.print()
