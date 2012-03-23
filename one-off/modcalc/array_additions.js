// fill in a range of an array with a single value
Array.prototype.fill = function (first, last, value) {
    var i;
    for (i = first; i <= last; i++) {
        this[i] = value;
    }
}

// remove all "undefined"s from an array
Array.prototype.cleanup = function () {
    var i = 0;
    while (i < this.length) {
        if (!this[i]) {
            this.splice(i,1);
        } else {
            i++;
        }
    }
}

// convert an array to a string with the given delimiter
Array.prototype.toString = function (delim) {
    var ret = "";
    var i;
    for (i = 0; i < this.length; i++) {
        if (i > 0) {
            ret = ret.concat(delim);
        }
        ret = ret.concat(this[i]);
    }
    return ret;
}