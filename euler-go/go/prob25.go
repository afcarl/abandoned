package euler

import (
	"math/big"
)

func fastFibonacci() chan *big.Int {
	ch := make(chan *big.Int)
	go func() {
		fnm1 := big.NewInt(0)
		fn := big.NewInt(1)
		for {
			ch <- new(big.Int).Set(fn)
			fn.Add(fn, fnm1)
			fnm1.Sub(fn, fnm1)
		}
	}()
	return ch
}
