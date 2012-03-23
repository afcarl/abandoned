package main

import (
    "./bitvec"
    "fmt"
)

func main() {
    vec := bitvec.CreateBitVector(100)
    fmt.Println(vec)
    vec.SetBit(63)
    vec.SetBit(17)
    vec.SetBit(97)
    fmt.Println(vec)
}
