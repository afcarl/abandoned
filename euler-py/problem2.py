#!/usr/bin/python

import sys

# problem 2: By considering the terms in the Fibonacci sequence whose values
# do not exceed four million, find the sum of the even-valued terms.

def main(args):
    sum = 2
    a = 1
    b = 2
    while a + b < 4000000:
        c = a + b
        if c % 2 == 0:
            sum += c
        a = b
        b = c
    print sum

if __name__ == '__main__':
    main(sys.argv[1:])