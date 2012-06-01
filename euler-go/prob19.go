package euler

const (
    JAN = iota
    FEB = iota
    MAR = iota
    APR = iota
    MAY = iota
    JUN = iota
    JUL = iota
    AUG = iota
    SEP = iota
    OCT = iota
    NOV = iota
    DEC = iota
)

var DAYS = [12]int {
    31, // jan
    28, // feb
    31, // mar
    30, // apr
    31, // may
    30, // jun
    31, // jul
    31, // aug
    30, // sep
    31, // oct
    30, // nov
    31, // dec
}

const LEAP = 29
const LEAPMONTH = FEB

const (
    MON = iota
    TUE = iota
    WED = iota
    THU = iota
    FRI = iota
    SAT = iota
    SUN = iota
)

const DAYS_PER_WEEK = 7

func isLeapYear(year int) bool {
    return (year % 4 == 0) && (year % 100 != 0 || year % 400 == 0)
}

func daysInMonth(month, year int) int {
    if month == LEAPMONTH && isLeapYear(year) {
        return LEAP
    }
    return DAYS[month]
}

func daysInYear(year int) int {
    if isLeapYear(year) { return 366 }
    return 365
}

func dayOfDate(date, month, year, firstDay, firstYear int) int {
    day := firstDay
    // advance to year
    for currentYear := firstYear; currentYear < year; currentYear++ {
        day = (day + daysInYear(currentYear)) % DAYS_PER_WEEK
    }
    // advance to month
    for currentMonth := JAN; currentMonth < month; currentMonth++ {
        day = (day + daysInMonth(currentMonth, year)) % DAYS_PER_WEEK
    }
    // advance to date
    for currentDate := 1; currentDate < date; currentDate++ {
        day = (day + 1) % DAYS_PER_WEEK
    }
    return day
}

const (
    firstDay = MON
    firstYear = 1900
    rangeStartDate = 1
    rangeStartMonth = JAN
    rangeStartYear = 1901
    rangeEndDate = 31
    rangeEndMonth = DEC
    rangeEndYear = 2000
    dayOfInterest = SUN
)
