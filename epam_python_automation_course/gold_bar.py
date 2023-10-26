import argparse
from itertools import combinations_with_replacement, permutations

parser = argparse.ArgumentParser()
parser.add_argument("-W",  help="capacity of the knapsack", type=int, required=True)
parser.add_argument("-w",  help="weights of the bars", type=int, nargs="+", required=True)
parser.add_argument("-n",  help="number of bars", type=int, required=True)
arguments = parser.parse_args()


def matrix_builder(number_of_bars):
    matrix = []
    combination = combinations_with_replacement(range(0, number_of_bars + 1), number_of_bars)
    for comb in list(combination):
        permutation = permutations(comb)
        for perm in list(permutation):
            if sum(perm) == number_of_bars:
                matrix.append(perm)
    return list(dict.fromkeys(matrix))


def gold_sack(capacity, weights, number_of_bars):
    graph = matrix_builder(number_of_bars)
    result_max = 0
    for row in graph:
        results = 0
        for i in range(0, number_of_bars):
            results += row[i] * weights[i]
            if (results > result_max) and (results <= capacity):
                result_max = results
                result_set = row
    print('The maximum amount of gold is: ' + str(result_max) + ' kg in the ' + str(capacity) + ' kg sack, which is contains the following piece(s) of bars: ')
    for kg in range(0, len(result_set)):
        print('- ' + str(result_set[kg]) + ' piece(s) of ' + str(weights[kg]) + ' kg bar')
    return result_max


if not (arguments.W or arguments.w or arguments.n):
    raise ValueError('Invalid argument')


gold_sack(arguments.W, arguments.w, arguments.n)
