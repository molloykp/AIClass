import numpy as np
import argparse
import matplotlib.pyplot as plt

"""
    Lab on Hill Climbers for NQueens
"""
from HillClimberProblem import SearchProblem

"""
Code to center the x-axis labels underneath the bars
of a graph
"""

def bins_labels(bins, **kwargs):
    bin_w = (max(bins) - min(bins)) / (len(bins) - 1)
    plt.xticks(np.arange(min(bins)+bin_w/2, max(bins), bin_w), bins, **kwargs)
    plt.xlim(bins[0], bins[-1])


class NQueensProblem(SearchProblem):
    """The problem of placing N queens on an NxN board with none attacking
    each other. A state is represented as an N-element array, where
    a value of r in the c-th entry means there is a queen at column c,
    row r, and a value of -1 means that the c-th column has not been
    filled in yet. We fill in columns left to right.
    >>> depth_first_tree_search(NQueensProblem(8))
    <Node (7, 3, 0, 2, 5, 1, 6, 4)>
    """

    def __init__(self, N):
        self.board = list([0] * N)
        self.N = N

    def getStartState(self):
        return self.board, self.h(self.board)

    """
    Change this method so that it generates a start state with randomly placed queens
    """

    def getStartRandom(self):
        pass

    def isGoalState(self, state):
        return not any(self.conflicted(state, state[col], col)
                       for col in range(len(state)))

    """
        return state(board), cost (conflicts)
    """
    def getSuccessors(self, state):
        stateArray = [0] * self.N**2

        for col in range(self.N):
            for row in range(self.N):
                newBoard = list(state[0])
                newBoard[col] = row
                stateArray[col*self.N + row] = (tuple(newBoard), self.h(newBoard))

        return stateArray


    def conflicted(self, state, row, col):
        """Would placing a queen at (row, col) conflict with anything?"""
        return any(self.conflict(row, col, state[c], c)
                   for c in range(col))

    def conflict(self, row1, col1, row2, col2):
        """Would putting two queens in (row1, col1) and (row2, col2) conflict?"""
        return (row1 == row2 or  # same row
                col1 == col2 or  # same column
                row1 - col1 == row2 - col2 or  # same \ diagonal
                row1 + col1 == row2 + col2)  # same / diagonal

    def h(self, state):
        """Return number of conflicting queens for a given state"""
        num_conflicts = 0
        for (r1, c1) in enumerate(state):
            for (r2, c2) in enumerate(state):
                if (r1, c1) != (r2, c2):
                    num_conflicts += self.conflict(r1, c1, r2, c2)

        return num_conflicts

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='NQueens Hill Climber')
    parser.add_argument('--nqueens', action='store',
                            dest='nqueens', default=8, required=False,
                            help='size of one dimension of the board')
    return parser.parse_args()

def main():

    """
    Write code to run 30 instances of this problem
    track the number of successful solutions found
    """
    parms = parse_arguments()
    # generate a history of solution quality
    # and place the quality of each configuration
    # found by the hill climber (the number of conflicts
    # is the quality).  Append each value to the
    # list obj_func declared below.

    obj_func = []


    """
    plt.plot()
    bin_list = range(8)
    nb, bins, patches = plt.hist(obj_func, bins =bin_list)
    plt.title('NQueens(' + str(parms.nqueens) + ') Objective Function')
    plt.ylabel('count',fontsize=16)
    plt.xlabel('h(state)',fontsize=16)
    bins_labels(bin_list, fontsize=20)

    plt.savefig(fname='nqueens' + str(parms.nqueens) + '.pdf', dpi=300,
                bbox_inches='tight',pad_inches=0.05)

    #plt.show() # uncomment to see the plot after the searches conclude
    """


if __name__ == "__main__":
    main()
