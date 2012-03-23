package bitvec

import (
    "fmt"
    "strings"
    "os"
)

type BitVector []uint64

type OutOfRangeError struct {
    bit uint
}

func (e *OutOfRangeError) String() string {
    return fmt.Sprintf("Bit %d is out of range!", e.bit)
}

// Functions for manipulating sets represented by bit vectors.

func CreateBitVector(max uint) BitVector {
    return BitVector(make([]uint64, max / 64 + 1))
}

func (vec *BitVector) GetBit(bit uint) (uint, os.Error) {
    i := bit / 64
    j := bit % 64
    if i >= uint(len(*vec)) {
        return 0, &OutOfRangeError{bit}
    }
    return uint(((*vec)[i] & (1 << j)) >> j), nil
}

func (vec *BitVector) SetBit(bit uint) os.Error {
    i := bit / 64
    j := bit % 64
    if i > uint(len(*vec)) {
        return &OutOfRangeError{bit}
    }
    (*vec)[i] |= 1 << j
    return nil
}

func (vec *BitVector) UnsetBit(bit uint) os.Error {
    i := bit / 64
    j := bit % 64
    if i > uint(len(*vec)) {
        return &OutOfRangeError{bit}
    }
    (*vec)[i] &= ^(1 << j)
    return nil
}

func (vec BitVector) String() string {
    words := make([]string, len(vec))
    for i, word := range vec {
        words[i] = fmt.Sprintf("%b ", word)
    }
    return strings.Join(words, " ")
}

// The following functions support the use of bit vectors where each bit
// can occur at most a bounded number of times.

type NBitVector struct {
    vec BitVector
    count uint
}

func CreateNBitVector(max, occurrences uint) *NBitVector {
    // need log(occurrences) bits to represent up to (excluding) occurrences
    bits := uint(0)
    for ; occurrences > 0; occurrences >>= 1 {
        bits++
    }
    return &NBitVector{BitVector(make([]uint64, (max / 64 + 1) * bits)), bits}
}

func (nvec *NBitVector) GetBitCount(bit uint) uint {
    base := bit * nvec.count
    high := base + nvec.count
    num := uint(0)
    for i := base + nvec.count - 1; i >= base && i < high; i-- {
        num <<= 1
        if val, _ := nvec.vec.GetBit(i); val > 0 {
            num |= 1
        }
    }
    return num
}

func (nvec *NBitVector) IncrementBitCount(bit uint) {
    // find first zero bit, set it, and clear bits to right
    base := bit * nvec.count
    high := base + nvec.count
    for i := base; i < base + nvec.count; i++ {
        if val, _ := nvec.vec.GetBit(i); val == 0 {
            nvec.vec.SetBit(i)
            for j := i-1; j >= base && j < high; j-- {
                nvec.vec.UnsetBit(j)
            }
            break
        }
    }        
}

func (nvec *NBitVector) DecrementBitCount(bit uint) {
    // find first one bit, unset it, and set all bits to right
    base := bit * nvec.count
    high := base + nvec.count
    for i := base; i < base + nvec.count; i++ {
        if val, _ := nvec.vec.GetBit(i); val == 1 {
            nvec.vec.UnsetBit(i)
            for j := i-1; j >= base && j < high; j-- {
                nvec.vec.SetBit(j)
            }
            break
        }
    }        
}
