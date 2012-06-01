package euler

func tripletsSumming(sum int) (a, b, c int) {
    for a := 1; a < sum; a++ {
        for b := a + 1; b < sum - a; b++ {
            c := sum - a - b
            if a*a + b*b == c*c {
                return a, b, c
            }
        }
    }
	return 0, 0, 0
}

