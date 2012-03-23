package main

import (
    "os"
    "fmt"
    "./bitvec"
)

const MAX = 10000000

func main() {
    vec := bitvec.CreateBitVector(MAX)
    max := uint(0)
    for {
        var num uint
        n, err := fmt.Scan(&num)
        if err == os.EOF { break }
        if n > 0 {
            vec.SetBit(num)
            if num > max { max = num }
        }
    }
    for i := uint(0); i <= max; i++ {
        if val, _ := vec.GetBit(i); val > 0 {
            fmt.Println(i)
        }
    }
}
