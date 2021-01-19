#
# Machine Learning
# Sample code for testing python
# To run from the UNIX prompt:  python3 testPython.py
# The program may create a warning message (which you can ignore)
# The program should create a PDF named testPython.pdf

import numpy as np
import sys
import random
import matplotlib.pyplot as plt

# Create an array of 1000 random numbers
X = np.random.rand(1000)

# Create a histogram of these numbers
n, bins, patches = plt.hist(x=X, bins='auto', color='blue',
                            alpha=0.7, rwidth=0.85)

# plot the histogram (test matplotlib)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Distribution of 1000 Points')
fileName = 'testPython.pdf'

plt.savefig(fileName,dpi=400,bbox_inches='tight',pad_inches=0.05) # save as a pdf

