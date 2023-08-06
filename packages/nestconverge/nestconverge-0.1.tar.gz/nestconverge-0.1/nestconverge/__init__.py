#!/usr/bin/python3

import numpy as np
import sys

def load_chains(path_to_chain='None'):
    ''' Asks user for path, and output the weights'''

    if path_to_chain == 'None':
        path = input('Introduce path to chains: ')
    else:
        path = path_to_chain

    while path[-1] == ' ':
        path = path[:-1]

    if path[-4:] != '.txt':    
        path += '.txt'

    try:
        weights = np.loadtxt(path, usecols = [0], unpack=True)
    except:
        print('No chains found at ', path)
        print('Make sure you specified the correct path')
        print('For example: ./chains/name_of_chain or ./chains/name_of_chain.txt')
        sys.exit()
    return weights

def print_convergence(weights, verbose = True, limit = 0.1):
    R_ns = weights[-1]
    print('R = %s' % float('%.2g' % weights[-1]))

    if verbose == True:
        if R_ns > limit:
            print('Convergence has not been achieved, resume chain with a lower tolerance')
        elif R_ns < limit:
            print('Convergence has been achieved')

def check(path):
    weights = load_chains(path_to_chain=path)
    print_convergence(weights)

if __name__ == '__main__':
    weights = load_chains()
    print_convergence(weights)
