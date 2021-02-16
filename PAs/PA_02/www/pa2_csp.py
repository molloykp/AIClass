"""
   name: cs444_csp.py
purpose: Load test files and then call CSP method(s)
"""



import sys
import argparse
import time
import numpy as np
from dataclasses import dataclass
import pickle

@dataclass
class NodeData:
    color: int
    neighbor_list: list



def parse_args():
    parser = argparse.ArgumentParser(description='CSP program that implemented min-conflicts and graph coloring')

    parser.add_argument('--inputFile', action='store',
                        dest='input_file_name', default="", required=True,
                        help='csv file of nodeId, neighborID')

    parser.add_argument('--colorCount', action='store',
                        dest='color_count', default="", required=True,
                        help='starting value for k (number of colors)', type=int)

    parser.add_argument('--solutionFile', action='store',
                        dest='solution_file_name', default="", required=True,
                        help='pickle of the solution')

    return parser.parse_args()


def mod_adj_list(adj_list, u, v):
    this_node = adj_list.get(u, None)
    if this_node is None:
        this_node = NodeData(-1,[])
        adj_list[u] = this_node

    if v not in this_node.neighbor_list:
        this_node.neighbor_list.append(v)




"""
Read in adjacency matrix and return a dictionary. 
keys in the dictionary are the nodeIDs of the graph
values are the list of neighb
"""

def parse_adj_file(input_file:str):
    print('processing file:', input_file)

    file = open(input_file, 'r')

    adj_list = {}
    first_line = True
    for line in file:
        if not first_line:
            line_items = line.split(',')
            u = line_items[0].rstrip()
            v = line_items[1].strip()
            if u != v: # no self edges
                mod_adj_list(adj_list, u, v)  # treat edge as undirected
                mod_adj_list(adj_list, v, u)
        else:
            first_line = False

    return adj_list


"""
A set of utility functions that you may optionally use in your implementation.
"""

identity = lambda x: x
def argmin_random_tie(seq, key=identity):
    """Return a minimum element of seq; break ties at random."""
    return min(shuffled(seq), key=key)

def shuffled(iterable):
    """Randomly shuffle a copy of iterable."""
    items = list(iterable)
    np.random.shuffle(items)
    return items




def min_conflicts (adj_list, color_count):
    """
    Implement min_conflicts.
    :return:     return true if solution found (and of course adj_list will contain the solution).
            otherwise, return false

    """

    raise NotImplementedError

def csp_solver(graph_file_name, color_count, solution_file_name):
    """
    Solve a csp that has only binary constraints.

    :param graph_file_name: CSV file that contains encodes the constraint graph
    :param color_count: The number of colors available for the CSP
    :param solution_file_name: output file that will encode the solution (pickle)
    :return: None
    """

    adj_list = parse_adj_file(graph_file_name)

    # Some stats aboout the constraint graph
    max_degree = max([len(items.neighbor_list) for items in adj_list.values()])
    edge_count = sum([len(items.neighbor_list) for items in adj_list.values()])

    print('Graph stats: nodes:', len(adj_list.keys()), ' edges:', edge_count,
      ' maxDegree is:', max_degree)

    # color_count is the initial value to start k (the number of colors)

    solution_flag = min_conflicts(adj_list, color_count)

    if solution_flag:
        # construct the solution
        solution = {}
        print('saving the solution')
        for node in adj_list.keys():
            solution[node] = adj_list[node].color

        with open(solution_file_name, 'wb') as handle:
            pickle.dump(solution, handle)
    else:
        print('No solution found')


def main():
    parms = parse_args()

    csp_solver(parms.input_file_name, parms.color_count, parms.solution_file_name)

if __name__ == '__main__':
    main()
