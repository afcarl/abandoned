#!/usr/bin/python

import math
import sys

# problem 4: Find the largest palindrome made from the product of two 
# 3-digit numbers.

def is_palindrome(num):
    seq = str(num)
    return seq[::-1] == seq

def main(args):
    largest = 0
    for i in range(100, 1000):
        for j in range(i, 1000):
            num = i * j
            if is_palindrome(num) and num > largest:
                largest = num
    print largest

if __name__ == '__main__':
    main(sys.argv[1:])