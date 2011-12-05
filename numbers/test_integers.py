#!/usr/bin/env python2.7

import unittest
import random
import integers

class IntegersTest(unittest.TestCase):
    def test_getprimes(self):
        expected = [2, 3, 5, 7, 11, 13, 17, 19,
                    23, 29, 31, 37, 41, 43, 47]
        actual = integers.getprimes(50)
        self.assertEqual(expected, actual)

    def test_factorize(self):
        primes = integers.getprimes(50)
        num = 1
        expected = []
        for prime in primes:
            power = random.randint(0, 5)
            if power == 0: continue
            expected.append((prime, power))
            num *= (prime ** power)
        actual = integers.factorize(num, primes)
        self.assertEqual(expected, actual)

    def test_factorial(self):
        num = 20
        expected = 2432902008176640000
        actual = integers.factorial(num)
        self.assertEqual(expected, actual)

    def test_fibonacci(self):
        expected = 6765
        actual = integers.fibonacci(20)
        self.assertEqual(expected, actual)

    def test_gcd(self):
        a = 2 * 5 * 11 * 19 * 29 * 31 * 47
        b = 3 * 7 * 13 * 23 * 29 * 37 * 43
        expected = 29
        actual1 = integers.gcd(a, b)
        actual2 = integers.gcd(b, a)
        actual3 = integers.gcd(-a, b)
        actual4 = integers.gcd(a, -b)
        actual5 = integers.gcd(-a, -b)
        self.assertEqual(expected, actual1)
        self.assertEqual(expected, actual2)
        self.assertEqual(expected, actual3)
        self.assertEqual(expected, actual4)
        self.assertEqual(expected, actual5)
        
        expected = 0
        actual1 = integers.gcd(27, 0)
        actual2 = integers.gcd(0, 27)
        self.assertEqual(expected, actual1)
        self.assertEqual(expected, actual2)

    def test_extended_euclid(self):
        a = 1970870
        b = 232323
        g = 23
        x, y = (-4496, 38141)
        self.assertEqual(g, x * a + y * b)
        actual = integers.extended_euclid(a, b)
        self.assertEqual((g, x, y), actual)

    def test_solve_diophantine(self):
        a = 1970870
        b = 232323
        g = 23
        x, y = (-4496, 38141)
        c = 5 * g
        expected = (5 * x, 5 * y)
        actual = integers.solve_diophantine(a, b, c)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
