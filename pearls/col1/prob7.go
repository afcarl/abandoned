package main

import (
    "./bitvec"
    "fmt"
    "os"
)

const MAX = 10000000

// problem 7: robustness and error-checking
func main() {
    vec := bitvec.CreateBitVector(MAX)
    max := uint(0)
    var num uint
    for {
        n, err := fmt.Scan(&num)
        if err == os.EOF {
            break
        } else if n == 0 {
            fmt.Fprintf(os.Stderr, "Encountered invalid input!\n")
            os.Exit(1)
        } else if num > MAX {
            fmt.Fprintf(os.Stderr, "Input too large; %d > %d\n", num, MAX)
            os.Exit(1)
        } else if vec.SetBit(num) != nil {
            fmt.Fprintf(os.Stderr, "%s\n", err)
            os.Exit(1)
        } else if num > max {
            max = num
        }
    }

    for i := uint(0); i <= max; i++ {
        if val, _ := vec.GetBit(i); val > 0 {
            fmt.Println(i)
        }
    }
}
