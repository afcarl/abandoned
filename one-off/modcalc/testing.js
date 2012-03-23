document.writeln("Hello");

var testcase_expr = {
    "(5+4+3*2-1+7*9-6*5)" : 47,
    "-(-(9-3) * (-21*-4) ^ 3) + ((57+4)^2 * -3)" : 3545061,
    "-((-9-3) * (-21*-4) ^3) + ((57+4)^2 * -3)" : 7101285,
    "-((9-3) * (-21*-4)^ 3) + -((57+-4)^2 * -3)" : -3547797,
    "-((9-3) * (-21*-4) ^ 3) + ((-57+4)^2 * -3)" : -3564651,
    "-((9-3) * (-21*-4)^3) + ((-57+-4)^2 * -3)" : -3567387,
    "-((9-3) * -(-21*-4) ^ 3) + (-(57+4)^2 * -3)" : 3567387,
    "-((9-3)*(-21*-4) ^ 3) + -(-(57+4)^2 * -3) + 14 - 2*-9" : -3567355,
    "-((9-3) * -(-21*-4) ^ 3) - -(-(57+4)^2 *-3)" : 3567387,
    "-((9-3) * -(-21*-4) ^ 3) + (-(57+4)^2 * -3)" : 3567387,
    "5+4 * 7 -((9-3)*(-21*-4) ^ 3) + -(-(57+4)^2 * -3)" : -3567354,
    "-((9-2* 3) * -(-21*-4 - 6 * 3) ^ 3) - 5 -(-(57+4)^2 *-3)" : 851320,
    "27 ^ 2 - 4*9*-5 + 32^1^2 + 6*7-9" : 1966,
};

var testcase_gcd = [[42,56,14], [48,180,12]];
var testcase_dio = [[77,42,35],[6,9,21]];

setVerbose(true);
for (expr in testcase_expr) {
    document.writeln("=================================================");
    document.writeln("Input: " + expr);
    var value = calculate(expr);
    var passed = (testcase_expr[expr] === value) ? "PASSED" : "FAILED";
    document.writeln(value + " ?== " + testcase_expr[expr]);
    document.writeln("TEST " + passed);
}

var i;
for (i = 0; i < testcase_gcd.length; i++) {
document.writeln("=================================================");
    var a = testcase_gcd[i][0];
    var b = testcase_gcd[i][1];
    var expected = testcase_gcd[i][2];
    
    var g = gcd(a, b);
    document.writeln("gcd(" + a + "," + b + ") = " + g + " ?== " + expected);
    if (g !== expected) {
        document.writeln("TEST FAILED");
    } else {
        document.writeln("TEST PASSED");
    }
}

for (i = 0; i < testcase_dio.length; i++) {
document.writeln("=================================================");
    var a = testcase_dio[i][0];
    var b = testcase_dio[i][1];
    var c = testcase_dio[i][2];
    
    var soln = dioSolve(a, b, c);
    var x = soln[0];
    var y = soln[1];
    
    document.writeln(c + " ?== " + soln[0] + "*" + a + " + " + soln[1] + "*" + b);
    if (x*a + y*b === c) {
        document.writeln("TEST PASSED");
    } else {
        document.writeln("TEST FAILED: " + x + "*" + a + " + " + y + "*" + b + " === " + (x*a+y*b) + " !== " + c);
    }
}