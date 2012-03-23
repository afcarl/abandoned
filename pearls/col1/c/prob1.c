#include <stdio.h>
#include <stdlib.h>

#define N 1000000

int intcmp(const void *x, const void *y) {
    return *(int *)x - *(int *)y;
}

int main(int argc, char *argv[]) {
    int data[N];
    int i, n;

    while ((i = scanf("%d", &data[n])) != EOF) {
        if (i == 1) {
	    n++;
	}
    }

    qsort(data, n, sizeof(int), intcmp);

    for (i = 0; i < n; i++) {
        printf("%d\n", data[i]);
    }

    return EXIT_SUCCESS;
}
