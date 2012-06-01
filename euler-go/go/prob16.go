package euler

import (
	"math/big"
)

func sumPowDigits(base, pow int64) int {
	var num big.Int
	bigbase := big.NewInt(base)
	bigpow := big.NewInt(pow)
	num.Exp(bigbase, bigpow, nil)

	sum := 0
	for _, c := range num.String() {
		sum += int(c - '0')
	}

	return sum
}
