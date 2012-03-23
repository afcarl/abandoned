#!/usr/bin/python

import math
import sys

# problem 6: Find the difference between the sum of the squares of the first
# one hundred natural numbers and the square of the sum.

def sum_first_n(n):
    return n * (n+1) / 2

def sum_sq_first_n(n):
    return n * (n+1) * (2*n+1) / 6

def main(args):
    print pow(sum_first_n(100), 2) - sum_sq_first_n(100)

if __name__ == '__main__':
    main(sys.argv[1:])