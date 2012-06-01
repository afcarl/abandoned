package euler

func gcd(a, b uint) uint {
    if a == 0 {
        return b
    } else if b == 0 {
        return a
    } else if a == 1 || b == 1 {
        return 1
    }
    return gcd(b, a % b)
}

func gcdn(nums ...uint) uint {
    if len(nums) == 2 {
        return gcd(nums[0], nums[1])
    }
    return gcd(nums[0], gcdn(nums[1:]...))
}

func lcm(a, b uint) uint {
    return a * b / gcd(a, b)
}

func lcmn(nums ...uint) uint {
    if len(nums) == 2 {
        return lcm(nums[0], nums[1])
    }
    return lcm(nums[0], lcmn(nums[1:]...))
}
