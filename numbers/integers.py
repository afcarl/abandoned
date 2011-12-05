#!/usr/bin/env python2.7

def getprimes(n):
    """Returns a list of all prime integers less than n.  Uses the
    Sieve of Erastothenes method."""
    isprime = [True for num in xrange(n)]
    isprime[0] = False
    isprime[1] = False
    for num in xrange(2, n):
        if not isprime[num]:
            continue
        m = n / num
        top = m if m * num == n else m + 1
        for i in xrange(2, top):
            isprime[num * i] = False
    return [num for num in xrange(n) if isprime[num]]


def factorize(n, factors):
    """Returns the factorization of n over factors as a list of tuples.
    Each tuple consists of a (factor, power) pair that indicates that
    factor divides n power times but not n + 1 times; equivalently,
    n % (factor ** power) == 0 but n % (factor ** (power + 1)) != 0."""
    factorization = []
    for factor in factors:
        if n % factor == 0:
            power = 1
            while n % (factor ** (power + 1)) == 0:
                power += 1
            factorization.append((factor, power))
    return factorization


def factorial(n):
    """Returns the integer n!"""
    ret = 1
    for i in xrange(2, n + 1):
        ret *= i
    return ret


def fibonacci(n):
    """Returns the nth fibonacci number."""
    k = 0
    kp1 = 1
    for i in xrange(n):
        k, kp1 = kp1, k + kp1
    return k


def gcd(a, b):
    """Returns the greatest common divisor of a and b using Euclid's
    algorithm.  The returned divisor is always non-negative."""
    if a == 0 or b == 0:
        return 0
    if a < 0: a = -a
    if b < 0: b = -b
    while b > 0:
        r = a % b
        a = b
        b = r
    return a


def extended_euclid(a, b):
    """Returns a tuple of integers (g, x, y) such that g = ax + by."""
    if a == 0 or b == 0:
        return 0
    if a < 0: a = -a
    if b < 0: b = -b
    a0, b0 = a, b

    # record the sequence of steps a = qb + r
    results = {}
    remainders = []
    while b > 0:
        r = a % b
        q = (a - r) / b
        results[r] = (a, b, q)
        remainders.append(r)
        a = b
        b = r
    g = a # the gcd is the last nonzero remainder
    
    # for each r found during computation, find x, y such that
    # r = xa + yb where a and b are the original input.
    coefs = {}
    coefs[a0] = (1, 0)
    coefs[b0] = (0, 1)
    for r in remainders[:-1]:
        #
        # Recall that a = qb + r.  So r = a - qb.
        #
        # Look up xa, ya, xb, yb in coefs so that
        # a = xa*a0 + ya*b0 and b = xb*a0 + yb*b0.
        #
        # From these we have
        # r = (xa*a0 + ya*b0) + (-q*xb*a0 + -q*yb*b0)
        # r = a0 * (xa - q * xb) + b0 * (ya - q * yb)
        # xr = xa - q * xb
        # yr = ya - q * yb
        #
        a, b, q = results[r]
        xa, ya = coefs[a]
        xb, yb = coefs[b]
        xr = xa - q * xb
        yr = ya - q * yb
        coefs[r] = xr, yr

    # answer is xg, yg where g = xg*a0 + yg*b0
    xg, yg = coefs[g]
    return g, xg, yg


def solve_diophantine(a, b, c):
    """Solves the linear diophantine equation ax + by = c, where all of
    a, b, c, x, y are integers.  Returns a solution as a tuple (x, y),
    or None if no solution exists."""
    g, x, y = extended_euclid(a, b)
    if c % g != 0: return None
    # we know that ax + by = g and that g|c
    m = c / g
    # so amx + bmy = mg = c
    return m * x, m * y
