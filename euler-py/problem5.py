#!/usr/bin/python

import math
import sys

# problem 5: What is the smallest positive number that is evenly divisible
# by all of the numbers from 1 to 20?

def gcd(a, b):
    while a % b > 0:
        c = a % b
        a = b
        b = c
    return b

def gcd_list(nums):
    g = nums[0]
    for num in nums[1:]:
        g = gcd(g, num)
    return g

def lcm(a, b):
    return a * b / gcd(a,b)

def lcm_list(nums):
    res = nums[0]
    for num in nums[1:]:
        res = lcm(res, num)
    return res

def main(args):
    print lcm_list(range(1,21))

if __name__ == '__main__':
    main(sys.argv[1:])