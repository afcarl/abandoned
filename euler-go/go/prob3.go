package euler

import (
    "math"
)

// note: not the fastest algorithm; a resizing sieve of erastothenes is better
func primes() chan int {
    ch := make(chan int)
    go func() {
        primes := make([]int, 0)
        for n := 2; ; n++ {
            isPrime := true
            for _, p := range primes {
                if n % p == 0 {
                    isPrime = false
                    break
                }
            }
            if isPrime {
                ch <- n
                primes = append(primes, n)
            }
        }
    }()
    return ch
}

func primeDivisors(num int64) []int {
    factors := make([]int, 0)
	max := int(math.Sqrt(float64(num)))
    for p := range primes() {
        if p > max { break }
        if num % int64(p) == 0 {
            factors = append(factors, p)
        }
    }
    return factors
}
