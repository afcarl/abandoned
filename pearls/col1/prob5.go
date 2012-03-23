package main

import (
    "fmt"
    "io"
    "os"
    "./bitvec"
)

// creates a bit vector of numbers falling in the range [min, max) that occur
// in the reader. bit i is set if min + i was observed.
func SlurpBoundedBitVector(r io.Reader, min, max uint) bitvec.BitVector {
    vec := bitvec.CreateBitVector(max - min)
    for {
        var num uint
        n, err := fmt.Fscanf(r, "%d", &num)
        if err == os.EOF { break }
        if n > 0 && num >= min && num < max { vec.SetBit(num - min) }
    }
    return vec
}

// scan the file multiple times, sorting the numbers in the range [min, max)
// in chunks with size chunk. prints to stdout.
func BoundedFileSort(filename string, min, max, chunk uint) {
    for i := min; i < max; i += chunk {
        file, err := os.Open(filename)
        if err == nil {
            vec := SlurpBoundedBitVector(file, i, i + chunk)
            for j := uint(0); j < chunk; j++ {
                if val, _ := vec.GetBit(j); val > 0 {
                    fmt.Println(j + i)
                }
            }
        }
    }
}    

func main() {
    filename := os.Args[1]
    BoundedFileSort(filename, 0, 10000000, 8000000)
}
