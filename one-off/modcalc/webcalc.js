var logResult = function (expr, mod, val) {
    var resultsTable = document.getElementById("results");
    var resultRow = resultsTable.insertRow(resultsTable.rows.length);
    resultRow.insertCell(0).innerHTML = expr;
    resultRow.insertCell(1).innerHTML = mod
    resultRow.insertCell(2).innerHTML = val;
}

var logError = function (expr) {
    logResult("Error: " + expr, "", "");
}

var evalEnter = function (e) {
    var keycode;
    
    if (window.event) {
        keycode = window.event.keyCode;
    } else if (e) {
        keycode = e.which;
    } else {
        return;
    }

    if (keycode === 13) {
        evalInput();
    }
}

var evalInput = function () {
    var expr = document.getElementById("inputExpr").value;
    var mod = document.getElementById("inputMod").value
    
    var modulus = parseInt(mod);
    if (!mod || modulus === NaN) {
        logError("No modulus!");
        return;
    }
    
    var val;
    try {
        val = calculate(expr, modulus);
    } catch (e) {
        logError(e);
        return;
    }
    
    logResult(expr, mod, val);
}
