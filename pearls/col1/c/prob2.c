#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "bitvec.h"

#define N 10000000

void printb(unsigned b) {
    if (!b) {
        return;
    }
    printb(b >> 1);
    putchar('0' + (b & 1));
}

void printlnb(unsigned b) {
    printb(b);
    putchar('\n');
}

int main(int argc, char *argv[]) {
    unsigned *vec = bitvec_create(N);
    bitvec_set(vec, 7);
    bitvec_set(vec, 12);
    bitvec_set(vec, 3);
    bitvec_set(vec, 70);
    bitvec_set(vec, 36);

    assert(bitvec_get(vec, 7) == 1);
    assert(bitvec_get(vec, 12) == 1);
    assert(bitvec_get(vec, 3) == 1);
    assert(bitvec_get(vec, 70) == 1);
    assert(bitvec_get(vec, 36) == 1);
    assert(bitvec_get(vec, 19) == 0);

    bitvec_unset(vec, 12);
    bitvec_unset(vec, 70);

    assert(bitvec_get(vec, 7) == 1);
    assert(bitvec_get(vec, 12) == 0);
    assert(bitvec_get(vec, 3) == 1);
    assert(bitvec_get(vec, 70) == 0);
    assert(bitvec_get(vec, 36) == 1);

    free(vec);
    return EXIT_SUCCESS;
}
