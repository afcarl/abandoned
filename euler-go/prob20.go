package euler

import (
	"math/big"
)

var ONE = big.NewInt(1)

func factorialSum(num int64) int {
	N := big.NewInt(num)
	acc := big.NewInt(1)
	for k := big.NewInt(1); k.Cmp(N) <= 0; k.Add(k, ONE) {
		acc.Mul(acc, k)
	}
	sum := 0
	str := acc.String()
	for _, c := range str {
		num := int(c - '0')
		sum += num
	}
	return sum
}
