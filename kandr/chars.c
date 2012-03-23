#include <assert.h>
#include <string.h>
#include <stdio.h>

int htoi(char s[]) {
    if (strlen(s) > 2 && s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
        return htoi(s + 2);
    }

    int val = 0;
    int i;
    for (i = 0; i < strlen(s); i++) {
        int c = s[i];
        if ('0' <= c && c <= '9') {
            val = 16 * val + (c - '0');
        } else if ('a' <= c && c <= 'f') {
            val = 16 * val + (c - 'a' + 10);
        } else if ('A' <= c && c <= 'F') {
            val = 16 * val + (c - 'A' + 10);
        } else {
            return 0;
        }
    }

    return val;
}

int main(int argc, char **argv) {
    assert(htoi("3C7") == 0x3c7);
    assert(htoi("3c7") == 0x3c7);
    assert(htoi("0x3c7") == 0x3c7);
    assert(htoi("0X3c7") == 0x3C7);
    assert(htoi("foo") == 0);
    assert(htoi("0xZXy") == 0);
}
