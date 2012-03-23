// determines whether a single character is a delimiting character
// delimiters: spaces, parens, operators
var isDelim = function (expr) {
    if (!expr || (typeof expr !== "string") || (expr.length !== 1)) {
        return false;
    }
    var delimRegexp = /[()\s\+\*^-]/;
    return delimRegexp.test(expr);
}

// determines whether a single character is an operation
var isOperation = function (expr) {
    if (!expr || (typeof expr !== "string") || (expr.length !== 1)) {
        return false;
    }
    var delimRegexp = /[\+\*^-]/;
    return delimRegexp.test(expr);
}

var isParens = function (expr) {
    if (!expr || (typeof expr !== "string") || (expr.length !== 1)) {
        return false;
    }
    var delimRegexp = /[()]/;
    return delimRegexp.test(expr);
}

// determines whether a single character is a whitespace character
var isWhite = function (expr) {
    if (!expr || (typeof expr !== "string") || (expr.length !== 1)) {
        return false;
    }
    var delimRegexp = /[\s]/;
    return delimRegexp.test(expr);
}

// determines whether a single character is numerical
var isNumerical = function (expr) {
    if (!expr || (typeof expr !== "string") || (expr.length !== 1)) {
        return false;
    }
    var delimRegexp = /[0-9]/;
    return delimRegexp.test(expr);
}

var isNumber = function (expr) {
    if (typeof expr === "number") {
        return true;
    }
    
    if (!expr || (typeof expr !== "string")) {
        return false;
    }
    
    var delimRegexp = /[-]?[0-9]+/;
    return delimRegexp.test(expr);
}