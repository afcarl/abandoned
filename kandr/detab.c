#include <stdio.h>
#include <stdlib.h>
#define TABSIZE 4

int main(int argc, char **argv) {
    int c;
    int col = 0;
    while ((c = getchar()) != EOF) {
        if (c == '\n') {
            col = 0;
            putchar('\n');
        } else if (c == '\t') {
            int tabs = TABSIZE - (col % TABSIZE);
            int i;
            for (i = 0; i < tabs; i++) {
                putchar(' ');
                col++;
            }
        } else {
            putchar(c);
            col++;
        }
    }

    return EXIT_SUCCESS;
}
