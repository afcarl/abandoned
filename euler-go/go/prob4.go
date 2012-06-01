package euler

import "fmt"

func productPalindromes(length int) chan int {
	ch := make(chan int)
	go func() {
		for x := 100; x <= 999; x++ {
			for y := x; y <= 999; y++ {
				num := x * y
				s := fmt.Sprint(num)
				palindrome := true
				length := len(s)
				for i := 0; i < length/2; i++ {
					if s[i] != s[length-i-1] {
						palindrome = false
						break
					}
				}
				if palindrome {
					ch <- num
				}
			}
		}
	}()
	return ch
}
