package euler

func sum(nums []uint64) (sum uint64) {
    for _, num := range nums { sum += num }
    return sum
}

func primeSieve(max uint64) (primes []uint64) {
	if max < 2 { return []uint64{} }
	
    isPrime := make([]bool, max)
    for i := range isPrime { isPrime[i] = true }
    isPrime[0], isPrime[1] = false, false

    // cross off all multiples of primes encountered
    for n := uint64(2); n < max; n++ {
        if isPrime[n] {
            primes = append(primes, n)
            for k := uint64(2); k*n < max; k++ {
                isPrime[k*n] = false
            }
        }
    }

    return primes
}
