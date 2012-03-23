#!/usr/bin/python

import sys

# problem 1: Find the sum of all the multiples of 3 or 5 below 1000.

def sum_multiples_lt_n(k, n):
    sum = 0
    i = 1
    while i*k < n:
        sum += i*k
        i += 1
    return sum

def main(args):
    print (sum_multiples_lt_n(3, 1000) 
           + sum_multiples_lt_n(5, 1000)
           - sum_multiples_lt_n(15, 1000))

if __name__ == '__main__':
    main(sys.argv[1:])