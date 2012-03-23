#!/usr/bin/python

import math
import sys

# problem 3: What is the largest prime factor of the number 600851475143?

def primes_less_than(num):
    nums = range(num) # list of integers
    is_prime = [True for i in xrange(num)] # list to delete composites
    is_prime[0] = False
    is_prime[1] = False
    
    i = 2
    while i < num:
        p = nums[i]
        # cross off all multiples
        j = 2
        while j * p < num:
            is_prime[j * p] = False
            j += 1
        # find next prime
        i += 1
        while i < num and not is_prime[i]:
            i += 1
    
    return [p for p in xrange(num) if is_prime[p]]

def main(args):
    num = 600851475143
    lim = int(math.sqrt(num))
    prime_factors = [p for p in primes_less_than(lim) if num % p == 0]
    print prime_factors[len(prime_factors) - 1]

if __name__ == '__main__':
    main(sys.argv[1:])