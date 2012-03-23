#include <stdio.h>
#include <stdlib.h>
#define TABSIZE 4
#define IN 1
#define OUT 0

int main(int argc, char **argv) {
    int state = OUT;
    int col = 0;
    int spaces = 0;
    
    int c;
    while ((c = getchar()) != EOF) {
        if (c == ' ') {
            state = IN;
            spaces++;
        } else {
            if (state == IN) {
                int leading = (TABSIZE - (col % TABSIZE)) % TABSIZE;
                leading = leading < spaces ? leading : spaces;
                int tabs = (spaces - leading) / TABSIZE;
                int trailing = spaces - leading - tabs * TABSIZE;

                col += spaces;
                while (leading--) {
                    putchar(' ');
                }
                while (tabs--) {
                    putchar('\t');
                }
                while (trailing--) {
                    putchar(' ');
                }
                
                state = OUT;
                spaces = 0;
            }
            
            putchar(c);
            if (c == '\t') {
                col += TABSIZE;
            } else if (c == '\n') {
                col = 0;
            } else {
                col++;
            }
        }
    }

    return EXIT_SUCCESS;
}
