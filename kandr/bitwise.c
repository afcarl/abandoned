#include <assert.h>
#include <stdio.h>

void printb(unsigned x) {
    if (x) {
        printb(x >> 1);
        putchar((x & 1) ? '1' : '0');
    }
}

void printlnb(unsigned x) {
    printb(x);
    putchar('\n');
}

unsigned setbits(unsigned x, int p, int n, unsigned y) {
    unsigned nmask = ~(~0 << n); /* rightmost n bits are 1, rest 0 */
    unsigned rangemask = ~(~0 << n) << (p - n + 1);
    unsigned zeroed = x & ~rangemask; /* replacement range zeroed out from x */
    unsigned ybits = (y & nmask) << (p - n + 1); /* replacement range from y */
    return zeroed | ybits;
}

unsigned invert(unsigned x, int p, int n) {
    unsigned nmask = ~(~0 << n);
    unsigned rangemask = nmask << (p - n + 1);
    unsigned flipped = ~(x & rangemask) & rangemask;
    unsigned zeroed = x & ~rangemask;
    return zeroed | flipped;
}

unsigned rightrot(unsigned x, int n) {
    return (x >> n) | (x << sizeof(x) * 8 - n);
}

int bitcount(unsigned x) {
    int count = 0;
    while (x) {
        x &= x - 1;
        count++;
    }
    return count;
}

int main(int argc, char **argv) {
    int a = 123;
    int b = 458;
    assert(setbits(a, 5, 3, b) == 83);
    assert(invert(a, 5, 4) == 71);
    assert(rightrot(b, 4) == 0xA000001C);
}
