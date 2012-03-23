package main

import (
    "fmt"
    "sort"
    "os"
)

const COUNT = 10000000

func main() {
    nums := make([]int, COUNT)
    count := 0
    for count < COUNT {
        var num int
        n, err := fmt.Scan(&num)
        if err == os.EOF { break }
        if n > 0 {
            nums[count] = num
            count++
        }
    }

    sort.Ints(nums[:count])
    for i := 0; i < count; i++ {
        fmt.Println(nums[i])
    }
}
