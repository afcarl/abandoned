package euler

import (
    "strings"
    "strconv"
)

const triangle1 = `
75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23`

var paths [][]int
func initMemoization(tri [][]int) {
    paths = make([][]int, len(tri))
    for i := 0; i < len(tri); i++ {
        paths[i] = make([]int, i+1)
    }
    paths[0][0] = tri[0][0]
}

func longestPath(tri [][]int, row, col int) int {
    if paths == nil { initMemoization(tri) }
    if paths[row][col] > 0 {
        return paths[row][col]
    }

    path := 0
    if col == 0 {
        path = longestPath(tri, row-1, 0) + tri[row][col]
    } else if col == row {
        path = longestPath(tri, row-1, col-1) + tri[row][col]
    } else {
        leftParent := longestPath(tri, row-1, col-1)
        rightParent := longestPath(tri, row-1, col)
        if leftParent > rightParent {
            path = leftParent + tri[row][col]
        } else {
            path = rightParent + tri[row][col]
        }
    }

    paths[row][col] = path
    return path
}

func readTriangle(triangle string) [][]int {
    rows := strings.Split(triangle, "\n")[1:]
    tri := make([][]int, len(rows))
    for i, row := range rows {
        nums := strings.Split(row, " ")
        tri[i] = make([]int, len(nums))
        for j := range nums {
            if num, ok := strconv.Atoi(nums[j]); ok == nil {
                tri[i][j] = num
            }
        }
    }
    return tri
}
