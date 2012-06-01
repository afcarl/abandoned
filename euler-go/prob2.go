package euler

func fibonacci() chan int {
    ch := make(chan int)
    go func() {
        fnm1 := 0
        fn := 1
        for {
            ch <- fn
            fnm1, fn = fn, fnm1 + fn
        }
    }()
    return ch
}
