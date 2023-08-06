#!/usr/bin/python3

import sys
import nestconverge

def main():
    if len(sys.argv) == 1: 
        weights = nestconverge.load_chains()
    elif len(sys.argv) == 2:
        weights = nestconverge.load_chains(sys.argv[1])
    else: 
        print('Too many arguments given. Call nestcheck with no arguments, or as:')
        print('nestconverge path_to_chains/name_of_chain.txt')
        sys.exit()

    nestconverge.print_convergence(weights)

