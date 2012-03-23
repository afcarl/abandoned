var modAdd = function (a, b, mod) {
    var ret = ((a % mod) + (b % mod)) % mod;
    return ret >= 0 ? ret : (ret+mod);
}

var modMult = function (a, b, mod) {
    var ret = ((a % mod) * (b % mod)) % mod;mod;
    return ret >= 0 ? ret : (ret+mod);
}

var gcd = function (a, b) {
    while (b > 1) {
        var q = (a/b) >= 0 ? Math.floor(a / b) : Math.ceil(a / b);
        var r = a % b;
        
        if (r === 0) {
            break;
        }
        
        a = b;
        b = r;
    }
    
    return b;
}

// solves the equation ax + by = c, if a solution exists (gcd(a,b)|c)
var dioSolve = function (a, b, c) {
    var a0 = a;
    var b0 = b;
    
    var remainders = [];
    var calculations = {};
    
    while (b > 1) {
        var q = (a/b) >= 0 ? Math.floor(a / b) : Math.ceil(a / b);
        var r = a % b;
        
        if (r === 0) {
            break;
        }
        
        remainders.push(r);
        calculations[r] = [a,b,q];
        
        a = b;
        b = r;
    }
    
    var gcd = b;
    if (c % gcd !== 0) {
        return;
    }
    
    var coefs = {};
    var i;
    for (i = 0; i < remainders.length; i++) {
        var r = remainders[i];
        var a = calculations[r][0];
        var b = calculations[r][1];
        var q = calculations[r][2];
        
        var xa, xb, ya, yb;
        
        if (a === a0) {
            xa = 1;
            ya = 0;
        } else if (a === b0) {
            xa = 0;
            ya = 1;
        } else {
            xa = coefs[a][0];
            ya = coefs[a][1];
        }
        
        if (b === a0) {
            xb = 1;
            yb = 0;
        } else if (b === b0) {
            xb = 0;
            yb = 1;
        } else {
            xb = coefs[b][0];
            yb = coefs[b][1];
        }
        
        // a = qb + r
        // r = a - qb
        // r = (xa*a0 + ya*b0) - q(xb*a0 + yb*b0)
        // r = (xa - q*xb)a0 + (ya - q*yb)*b0
        var x = xa - q*xb;
        var y = ya - q*yb;
        coefs[r] = [x, y];
    }
    
    var divisor = c / gcd;
    return [coefs[gcd][0]*divisor, coefs[gcd][1]*divisor];
}

// uses a diophantine equation solver to find the modular inverse
var modInv = function (a, mod) {
    var res = dioSolve(a, mod, 1);
    if (!res) {
        throw "No inverse of " + a + " exists mod " + mod + "!";
    }
    
    inv = res[0] >= 0 ? res[0] : (res[0]+mod);
    return inv;
}

// uses the fast modular exponentiation by repeated squaring algorithm
// if the power is negative, first finds the modular inverse (if exists)
var modExp = function (a, b, mod) {
    a = a % mod;
    a = (a >= 0 ? a : (a+mod));
    
    if (b < 0) {
        a = modInv(a, mod);
        b *= -1;
    } else if (b === 0) {
        return 1;
    }
    
    var res = 1;
    while (b > 0) {
        var x = a;
        var p = 1;
        while (p+p <= b) {
            x = (x*x) % mod;
            p = p+p;
        }
        
        res = (res * x) % mod;
        b = b - p;
    }
    
    return res >= 0 ? res : (res+mod);
}