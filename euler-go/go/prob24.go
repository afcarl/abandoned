package euler

// permutations: return permutations of str ordered lexiographically
func permutations(str string) chan string {
    ch := make(chan string)
    go func() {
        if len(str) < 2 {
            ch <- str
        } else if len(str) == 2 {
            ch <- str
            ch <- string(str[1]) + string(str[0])
        } else {
            // remove the ith element and permute the others
            for i, v := range str {
                others := str[:i] + str[i+1:]
                for perm := range permutations(others) {
                    ch <- string(v) + perm
                }
            }
        }
        close(ch)
    }()
    return ch
}
