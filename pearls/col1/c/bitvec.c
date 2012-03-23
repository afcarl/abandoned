#include <stdlib.h>
#include "bitvec.h"

unsigned *bitvec_create(int n) {
    int i;
    unsigned *vec;
    size_t width = sizeof(unsigned);
    int num = n / width;

    if (num * width < n) {
        num++;
    }

    vec = (unsigned *) malloc(num * width);
    for (i = 0; i < num; i++) {
        vec[i] = 0;
    }

    return vec;
}

void bitvec_set(unsigned *vec, int bit) {
    int i = bit / (sizeof(unsigned) * 8);
    int j = bit % (sizeof(unsigned) * 8);
    vec[i] |= 1 << j;
}

void bitvec_unset(unsigned *vec, int bit) {
    int i = bit / (sizeof(unsigned) * 8);
    int j = bit % (sizeof(unsigned) * 8);
    vec[i] &= ~(1 << j);
}

unsigned bitvec_get(unsigned *vec, int bit) {
    int i = bit / (sizeof(unsigned) * 8);
    int j = bit % (sizeof(unsigned) * 8);
    return (vec[i] & (1 << j)) > 0;
}    

