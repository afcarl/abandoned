package euler

func gridRoutes(rows, cols int) uint64 {
    paths := make([][]uint64, rows+1)
    for j := range paths {
        paths[j] = make([]uint64, cols+1)
    }
    
    for i := 0; i < cols+1; i++ {
        for j := i; j < rows+1; j++ {
            var val uint64
            if i == 0 && j == 0 {
                val = 0
            } else if i == 0 || j == 0 {
                val = 1
            } else {
                val = paths[i-1][j] + paths[i][j-1]
            }
            paths[i][j] = val
            paths[j][i] = val
        }
    }
	return paths[rows][cols]
}
