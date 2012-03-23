package main

import (
    "./bitvec"
    "fmt"
)

func checkBitCounts(bit uint) {
    vec := bitvec.CreateNBitVector(100, 10)
    for i := uint(0); i < 10; i++ {
        if vec.GetBitCount(bit) != i {
            fmt.Println("Failed!")
        }
        vec.IncrementBitCount(bit)
    }
    for i := uint(10); i > 0; i-- {
        if vec.GetBitCount(bit) != i {
            fmt.Println("Failed!")
        }
        vec.DecrementBitCount(bit)
    }
    if vec.GetBitCount(bit) != 0 {
        fmt.Println("Failed!")
    }
}

func main() {
    checkBitCounts(31)
    checkBitCounts(97)
    checkBitCounts(0)
    checkBitCounts(100)
}
