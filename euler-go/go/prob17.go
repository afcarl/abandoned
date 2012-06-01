package euler

var digits = []string {
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
}

var teens = []string {
    "ten", "eleven", "twelve", "thirteen", "fourteen",
    "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
}

var tens = []string {
    "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
}

var powers = []string {
    "hundred", "thousand",
}

func spell(num int) string {
    word := ""

    ones := num % 100
    if ones >= 10 && ones < 20 {
        word = teens[ones-10]
    } else {
        one := ones % 10
        ten := ones / 10
        if one > 0 {
            word = digits[one]
        }
        if ten > 0 {
            word = tens[ten-2] + word
        }
    }

    rest := num / 100
    if rest > 0 && ones > 0  { word = "and" + word }
    for place := 0; rest > 0; place++ {
        digit := rest % 10
        if digit > 0 {
            word = digits[digit] + powers[place] + word
        }
        rest /= 10
    }
    
    return word
}
