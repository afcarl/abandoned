package main

import (
    "rand"
    "fmt"
    "time"
)

const (
    MAX = 10000000
    COUNT = 1000000
)

func main() {
    rand.Seed(time.Seconds())
    nums := rand.Perm(MAX)[:COUNT]
    for _, val := range nums {
        fmt.Println(val)
    }
}
