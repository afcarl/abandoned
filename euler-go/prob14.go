package euler

var memo = make(map[uint64]uint64)
func iterate(n uint64) uint64 {
    length := uint64(1)
    for k := n; k > 1; length++ {
        if l, ok := memo[k]; ok {
            length += l - 1
            break
        }
        
        if k % 2 == 0 {
            k /= 2
        } else {
            k = 3*k + 1
        }
    }

    memo[n] = length
    return length
}
