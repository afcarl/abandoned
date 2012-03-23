var verbose = false;

var setVerbose = function (yes) {
    verbose = yes;
}

// parses an input expression into token strings using isDelim()
var tokenize = function (expr) {
    if (!expr || (typeof expr !== "string") || (expr.length === 0)) {
        return; // error, undefined
    }
    
    tokens = [];
    var i,j;
    for (i = 0, j = 0; j < expr.length; j++) {
        if (isDelim(expr[j]) || j == expr.length) {
            if (j > i) {
                var token = expr.substring(i,j);
                tokens.push(token);
            }
            
            if (!isWhite(expr[j])) {
                var delim = expr.substring(j,j+1);
                tokens.push(delim);
            }
            
            i = j + 1;
        } else if (!isNumerical(expr[j])) {
            throw "Invalid character: " + expr[j];
        }
    }
    
    if (j > i) {
        tokens.push(expr.substring(i,j));
    }

    return tokens;
};

var verify = function (tokens) {
    // check for back-to-back operators
    var i;
    for (i = 0; i < tokens.length; i++) {
        var t = tokens[i];
        
        // check for invalid token
        if (t === undefined || (!isNumber(t) && !isOperation(t) && !isParens(t))) {
            return "Invalid token: " + t;
        }
        
        // check for leading/trailing operations
        if (i === 0 && isOperation(t) && (t !== "-")) {
            return "Can't begin with operation: " + t;
        } else if (i === tokens.length-1 && isOperation(t)) {
            return "Can't end with operation: " + t;
        }
        
        // check for back-to-back operations
        if (i > 0 && i < tokens.length-1 && 
                isOperation(tokens[i]) && isOperation(tokens[i-1])) {
            // back-to-back operations... OK only if unary minus
            if (t !== "-" || !isNumber(tokens[i+1])) {
                return "No back to back operations! " + tokens[i-1] + t;
            }
        }
    }
    
}

var handleExp = function (tokens, mod) {
    var i;
    for (i = 0; i < tokens.length; i++) {
        if (tokens[i] === "^") {
            if (i === 0 || i == tokens.length-1) {
                throw "syntax error (exponentiation)";
            }

            var a = parseInt(tokens[i-1]);
            var b = parseInt(tokens[i+1]);
            tokens.splice(i-1, 3, modExp(a, b, mod));
            i--;
        }
    }
    
    if (verbose) {
        document.writeln("reduce/exp: " + tokens.toString(""));
    }
};

var handleAdd = function (tokens, mod) {
    var i;
    for (i = 0; i < tokens.length; i++) {
        if (tokens[i] === "+") {
            if (i === 0 || i == tokens.length-1) {
                throw "syntax error (addition)";
            }

            var a = parseInt(tokens[i-1]);
            var b = parseInt(tokens[i+1]);
            tokens.splice(i-1, 3, modAdd(a, b, mod));
            i--;
        }
    }
    
    if (verbose) {
        document.writeln("reduce/add: " + tokens.toString(""));
    }
};

var handleSub = function (tokens, mod) {
    var i;
    for (i = 0; i < tokens.length; i++) {
        if (tokens[i] === "-") {
            if (i == 0 || i == tokens.length-1) {
                throw "syntax error (subtraction)";
            }

            var a = parseInt(tokens[i-1]);
            var b = parseInt(tokens[i+1]);
            tokens.splice(i-1, 3, modAdd(a, -b, mod));
            i--;
        }
    }
    
    if (verbose) {
        document.writeln("reduce/sub: " + tokens.toString(""));
    }
};

var handleUnaryMinus = function (tokens) {
    var i;
    for (i = 0; i < tokens.length; i++) {
        if (tokens[i] === "-" && (i == 0 || !isNumber(tokens[i-1]))) {
            if (i == tokens.length-1 || !isNumber(tokens[i+1])) {
                throw "syntax error (unary minus)";
            }

            var a = parseInt(tokens[i+1]);
            tokens.splice(i,2,-a);
        }
    }
    
    if (verbose) {
        document.writeln("reduce/-: " + tokens.toString(""));
    }
};

var handleMult = function (tokens, mod) {
    var i;
    for (i = 0; i < tokens.length; i++) {
        if (tokens[i] === "*") {
            if (i === 0 || i == tokens.length-1) {
                throw "syntax error (multiplication)";
            }

            var a = parseInt(tokens[i-1]);
            var b = parseInt(tokens[i+1]);
            tokens.splice(i-1, 3, modMult(a, b, mod));
            i--;
        }
    }
    
    if (verbose) {
        document.writeln("reduce/mult: " + tokens.toString(""));
    }
};

var handleParens = function (tokens) {
    var i;
    for (i = 0; i < tokens.length; i++) {
        if (tokens[i] === "(") {
            // scan right for matching )
            var j;
            var pctr = 0;
            for (j = i+1; j < tokens.length; j++) {
                if (tokens[j] === ")") {
                    if (pctr === 0) {
                        var subtokens = tokens.slice(i+1,j);
                        var val = tokensEval(subtokens);
                        var deleted = j-i+1;
                        tokens.splice(i, deleted, val);
                        j = j - deleted;
                        break;
                    } else {
                        pctr--;
                    }
                } else if (tokens[j] === "(") {
                    pctr++;
                }
            }
        } else if (tokens[i] === ")") {
            throw "syntax error (parentheses)";
        }
    }
    
    if (verbose) {
        document.writeln("reduce/parens: " + tokens.toString(""));
    }
};

// evaluates an expression from a list of tokens
var tokensEval = function (tokens, mod) {
    if (!tokens || !tokens.length || mod === undefined) {
        return 0;
    }
    
    if (verbose) {
        document.writeln("expression: " + tokens.toString(""));
    }
    
    var i;
    
    handleParens(tokens);
    handleUnaryMinus(tokens);
    handleExp(tokens, mod);
    handleMult(tokens, mod);
    handleSub(tokens, mod);
    handleAdd(tokens, mod);
    
    if (tokens.length > 1) {
        // another pass
        return tokensEval(tokens, mod);
    } else {
        return tokens[0];
    }
};

var calculate = function (expr, mod) {
    var tokens = tokenize(expr);
    if (!tokens) {
        return 0;
    }
    
    var err = verify(tokens);
    if (err) {
        throw err;
    }
    
    return tokensEval(tokens, mod);
};
