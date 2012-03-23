#!/usr/bin/python

import math
import sys

# problem 7: What is the 10001st prime number?

def first_n_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        is_prime = True
        rt = math.sqrt(num)
        for prime in primes:
            if prime > rt:
                break
            if num % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
        num += 1
    return primes

def main(args):
    primes = first_n_primes(10001)
    print primes[len(primes) - 1]

if __name__ == '__main__':
    main(sys.argv[1:])