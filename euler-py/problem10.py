#!/usr/bin/python

import math
import sys

import problem3

# problem 10: Find the sum of all the primes below two million.

def main(args):
    primes = problem3.primes_less_than(2000000)
    print sum(primes)

if __name__ == '__main__':
    main(sys.argv[1:])