#include <stdio.h>
#include <stdlib.h>
#include "bitvec.h"

#define N 10000000

int main(int argc, char *argv[]) {
    int i;
    unsigned *vec = bitvec_create(N);
    
    while (scanf("%d", &i) != EOF) {
        bitvec_set(vec, i);
    }

    for (i = 0; i < N; i++) {
        if (bitvec_get(vec, i)) {
            printf("%d\n", i);
        }
    }
}
