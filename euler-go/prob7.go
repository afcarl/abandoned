package euler

// note: not the fastest algorithm; a resizing sieve of erastothenes is better
func nthPrime(n int) int {
    primes := make([]int, 0)
    for k, x := 0, 2; k < n; x = x+1 {
        isPrime := true
        for _, p := range primes {
            if x % p == 0 {
                isPrime = false
                break
            }
        }
        if isPrime {
            k++
            primes = append(primes, x)
        }
    }
    return primes[n-1]
}
