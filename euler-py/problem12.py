#!/usr/bin/python

import math
import sys

# problem 12: What is the value of the first triangle number to have over
# five hundred divisors?

# get a list of at all primes <= num
# uses sieve of eratoshenes method
def get_primes(num):
    if num < 2:
        return []

    primes = []
    is_prime = [True for i in xrange(num)]

    p = 2
    while p < num:
        # find next prime
        while p < num and not is_prime[p]:
            p += 1
        if p == num:
            break
        primes.append(p)
        # cross off multiples
        j = 2
        while j * p < num:
            is_prime[j * p] = False
            j += 1
        p += 1

    return primes

# find the prime factorization (with powers) of num as a list of 2-tuples
def prime_factors(num, primes):
    rt = math.sqrt(num)
    prime_divisors = []
    for prime in primes:
        if prime > rt:
            break
        if num % prime == 0:    
            prime_divisors.append(prime)
    
    factors = []
    for prime in prime_divisors:
        count = 0
        n = 1
        while num % pow(prime, n) == 0:
            count += 1
            n += 1
        factors.append((prime, count))
    
    return factors

# count the total number of divisors of n
def num_divisors(num, primes):
    factors = prime_factors(num, primes)
    count = 1
    for prime, power in factors:
        count *= power + 1
    return count

def main(args):
    primes = get_primes(pow(2,16))
    n = 1
    count = 0
    saved = {}
    while count <= 500:
        t = n*(n+1)/2
        if n % 2 == 0:
            factors1 = saved.setdefault(n/2, num_divisors(n/2, primes))
            factors2 = saved.setdefault(n+1, num_divisors(n+1, primes))
        else:
            factors1 = saved.setdefault(n, num_divisors(n, primes))
            factors2 = saved.setdefault((n+1)/2, num_divisors((n+1)/2, primes))
        count = factors1 * factors2
        n += 1
    print t

if __name__ == '__main__':
    main(sys.argv[1:])
