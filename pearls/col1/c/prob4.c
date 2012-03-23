#include <stdio.h>
#include <stdlib.h>
#include "bitvec.h"

#define COUNT 1000000
#define MAX 10000000

int main(int argc, char *argv[]) {
    int i = 0;
    unsigned *vec = bitvec_create(N);
    srand(time(NULL));
    while (i < M) {
	int x = rand() % N;
	if (!bitvec_get(vec, x)) {
	    bitvec_set(vec, x);
	    printf("%d\n", x);
	    i++;
	}
    }
}
