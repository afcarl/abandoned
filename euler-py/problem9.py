#!/usr/bin/python

import math
import sys

# problem 9: There exists exactly one Pythagorean triplet for which
# a + b + c = 1000. Find the product abc.

def main(args):
    # simper to test triples that sum to 1000 than to find all
    # pythagorean triples
    for c in range(1, 1000):
        # find pairs that sum to 1000-c
        for b in range(1, 1000-c):
            a = 1000 - c - b
            if pow(a, 2) + pow(b, 2) == pow(c, 2):
                print a*b*c
                return

if __name__ == '__main__':
    main(sys.argv[1:])