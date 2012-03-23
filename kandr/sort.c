#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Constants */

#define TRUE 1
#define FALSE 0
#define MAXLINE 1000
#define MAXLINES 1000

/* Function declarations */

int sort(void *v[], int left, int right, int (*cmp)(void *a, void *b));

int readline(char *s, int lim);
int readlines(char *s[], int lim);
void writelines(char *s[], int num);

/* Function implementations */

void swap(void *v[], int i, int j) {
    void *temp = v[i];
    v[i] = v[j];
    v[j] = temp;
}

int sort(void *v[], int left, int right, int (*cmp)(void *a, void *b)) {
    int i, last;
    if (left >= right) {
        return;
    }

    swap(v, left, left + (right - left) / 2); /* move pivot to left */
    last = left;
    for (i = left + 1; i <= right; i++) {
        /* v[left+1], ..., v[last] < pivot, v[last+1], ..., V[i-1] >= pivot */
        if (cmp(v[i], v[left]) < 0) {
            swap(v, ++last, i);
        }
    }

    swap(v, left, last);
    sort(v, left, last-1, cmp);
    sort(v, last+1, right, cmp);
}

int readline(char *s, int lim) {
    int i, c;
    for (i = 0; i < lim - 1 && (c = getchar()) != EOF && c != '\n'; i++) {
        s[i] = c;
    }
    if (i < lim - 1 && c == '\n') {
        s[i++] = '\n';
    }
    s[i] = '\0';
    return i;
}

int readlines(char *s[], int lim) {
    int i;
    for (i = 0; i < lim; i++) {
        char *line = (char *) malloc(MAXLINE * sizeof(char));
        if (readline(line, MAXLINE) == 0) {
            free(line);
            break;
        }
        s[i] = line;
    }
    return i;
}

void writelines(char *s[], int num) {
    int i;
    for (i = 0; i < num; i++) {
        printf("%s", s[i]);
    }
}

int revstrcmp(char *a, char *b) {
    return -strcmp(a,b);
}

/* Main */

int main(int argc, char *argv[]) {
    char *lines[MAXLINES];
    int read;
    int c, reverse = FALSE, ignorecase = FALSE;

    while (--argc > 0 && (*++argv)[0] == '-') {
        while (c = *++argv[0]) {
            switch (c) {
            case 'r':
                reverse = TRUE;
                break;
            case 'i':
                ignorecase = TRUE;
                break;
            default:
                fprintf(stderr, "Illegal option: %c\n", c);
                argc = 0;
                break;
            }
        }
    }

    if (argc != 0) {
        fprintf(stderr, "Usage: sort -r -i\n");
        return EXIT_FAILURE;
    }

    read = readlines(lines, MAXLINES);
    sort((void **) lines, 0, read-1, (int (*)(void *, void *)) strcmp);
    writelines(lines, read);
    
    return EXIT_SUCCESS;
}
