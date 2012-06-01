package euler

import (
    "math"
)

func triangle(n uint64) uint64 {
    return (n * (n + 1)) / 2
}

// returns z such that y^z divides x but y^(z+1) does not.
func countDivides(x, y uint64) uint64 {
    z := uint64(0)
    for x % y == 0 {
        z++
        x /= y
    }
    return z
}

// returns a list of [prime, power] pairs where prime ^ power divides n but
// prime ^ (power+1) does not.  factors over specified primes.
func factorize(primes []uint64, n uint64) (factors [][]uint64) {
    for n >= 2 {
        var factor []uint64
        // if n has no factor smaller than sqrt(n) then n is prime
        // so just check p < sqrt(n)
        for i := 0; primes[i] <= uint64(math.Sqrt(float64(n))); i++ {
            p := primes[i]
            if n % p == 0 {
                pow := countDivides(n, p)
                factor = []uint64{p, pow}
                factors = append(factors, factor)
                n /= uint64(math.Pow(float64(p), float64(pow)))
                break
            }
        }
        if factor == nil {
            factors = append(factors, []uint64{n, 1})
            break
        }
    }
    return factors
}

func combineFactors(factors [][]uint64) uint64 {
    n := uint64(1)
    for _, factor := range factors {
        n *= uint64(math.Pow(float64(factor[0]), float64(factor[1])))
    }
    return n
}

// number of divisors of x:
// find prime factorization of x as p1^n1 * p2^n2 * ... * pk^nk
// then number of divisors is (n1+1)*(n2+1)*...*(nk+1)
func countDivisors(primes []uint64, num uint64) uint64 {
    divisors := uint64(1)
    factors := factorize(primes, num)
    for _, factor := range factors {
        divisors *= factor[1] + uint64(1)
    }
	return divisors
}
