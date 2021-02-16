# pa2_autograder.py
# -------------

from pa2_csp import *

import argparse
import pickle
import sys

# load the data for the USA map


def parse_args():
    parser = argparse.ArgumentParser(description='CSP program that implemented min-conflicts and graph coloring')

    parser.add_argument('--inputFile', action='store',
                        dest='input_file_name', default="", required=True,
                        help='csv file of nodeId, neighborID')

    parser.add_argument('--colorCount', action='store',
                        dest='color_count', default="", required=True,
                        help='limit on colors', type=int)

    parser.add_argument('--solutionFile', action='store',
                        dest='solution_file_name', default="", required=True,
                        help='pickle of the solution')

    return parser.parse_args()



def check_solution(input_file_name, solution_file_name, max_colors):
    constraint_graph = parse_adj_file(input_file_name)

    print('loading solution:', solution_file_name)
    solution = pickle.load(open(solution_file_name, "rb"))

    utilized_colors = set()

    solution_ok = True
    for node in constraint_graph:
        if node not in solution:
            print('ERROR: Node missing from solution:', node)
            solution_ok = False
            continue

        for neighbor in constraint_graph[node].neighbor_list:
            if neighbor not in solution:
                solution_ok = False
                print('ERROR: node missing from solution:', neighbor)
                continue

            if solution[node] == solution[neighbor]:
                solution_ok = False
                print('ERROR: neighbors with same color detected:', node, neighbor,
                      'color:', solution[node])
            utilized_colors.add(constraint_graph[node].color)

    if len(utilized_colors) > max_colors:
        print('ERROR Number of colors is:', len(utilized_colors), 'max colors was:', max_colors)
        solution_ok = False

    return solution_ok

def main():
    parms = parse_args()

    if check_solution(parms.input_file_name,parms.solution_file_name, parms.color_count):
        sys.exit(0)
    else:
        print("Errors detected")
        sys.exit(200)
if __name__ == '__main__':
    main()
