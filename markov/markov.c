#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum {
    NPREF = 2, /* number of prefix words */
    NHASH = 4093, /* size of state hash table array */
    MAXGEN = 10000 /* maximum words generated */
};

char *NONWORD = "\n"; /* cannot appear as a real word */

struct state {
    char *pref[NPREF]; /* prefix words */
    struct suffix *suf; /* list of suffixes */
    struct state *next; /* next state in hash bucket */
};

struct suffix {
    char *word; /* suffix */
    struct suffix *next; /* next in list of suffixes */
};

struct state *statetab[NHASH]; /* hash table of states */

/* hash: compute hash value for array of NPREF strings */
unsigned int hash(char *s[NPREF]) {
    unsigned int h;
    unsigned char *p;
    int i;

    h = 0;
    for (i = 0; i < NPREF; i++)
	for (p = (unsigned char *) s[i]; *p != '\0'; p++)
	    h = 31 * h + *p;
    
    return h % NHASH;
}

/*
 * lookup: search for prefix; create if requested.
 *  returns pointer if present or created; NULL if not.
 *  creation doesn't strdup so strings mustn't change later.
 */
struct state *lookup(char *prefix[NPREF], int create) {
    int i, h;
    struct state *sp;

    h = hash(prefix);

    /* look for an existing state for prefix */
    for (sp = statetab[h]; sp != NULL; sp = sp->next) {
	for (i = 0; i < NPREF; i++)
	    if (strcmp(prefix[i], sp->pref[i]) != 0)
		break;
	if (i == NPREF) /* found the right state */
	    return sp;
    }

    if (create) {
	sp = malloc(sizeof(struct state));
	for (i = 0; i < NPREF; i++)
	    sp->pref[i] = prefix[i];
	sp->suf = NULL;
	sp->next = statetab[h];
	statetab[h] = sp;
    }
    return sp;
}

/* addsuffix: add to state. suffix must not change later */
void addsuffix(struct state *sp, char *suffix) {
    struct suffix *suf;

    suf = malloc(sizeof(struct suffix));
    suf->word = suffix;
    suf->next = sp->suf;
    sp->suf = suf;
}

/* add: add word to suffix list and update prefix */
void add(char *prefix[NPREF], char *suffix) {
    struct state *sp;

    sp = lookup(prefix, 1); /* create if not found */
    addsuffix(sp, suffix);

    /* shift prefix words */
    memmove(prefix, prefix+1, (NPREF-1)*sizeof(prefix[0]));
    prefix[NPREF-1] = suffix;
}

/* build: read input and build the prefix table */
void build(char *prefix[NPREF], FILE *f) {
    char buf[100], fmt[10];

    /* create a format string to read fixed number of bytes into buf */
    sprintf(fmt, "%%%lus", sizeof(buf)-1);
    while (fscanf(f, fmt, buf) != EOF)
	add(prefix, strdup(buf));
}

/* updatepref: shift the prefix words and add a new one */
void updatepref(char *prefix[NPREF], char *w) {
    memmove(prefix, prefix+1, (NPREF-1)*sizeof(prefix[0]));
    prefix[NPREF-1] = w;
}

/* generate: produce output, one word per line */
void generate(int nwords) {
    struct state *sp;
    struct suffix *suf;
    char *prefix[NPREF], *w;
    int i, nmatch;

    for (i = 0; i < NPREF; i++) /* reset initial prefix */
	prefix[i] = NONWORD;

    for (i = 0; i < nwords; i++) {
	sp = lookup(prefix, 0);
	nmatch = 0;
	for (suf = sp->suf; suf != NULL; suf = suf->next)
	    if (rand() % ++nmatch == 0) /* prob = 1/nmatch */
		w = suf->word;
	if (strcmp(w, NONWORD) == 0)
	    break;
	printf("%s ", w);
	memmove(prefix, prefix+1, (NPREF-1)*sizeof(prefix[0]));
	prefix[NPREF-1] = w;
    }

    printf("\n");
}

int main(int argc, char *argv[]) {
    int i, nwords;
    char *prefix[NPREF];

    /* initialize random number generator */
    srand(time(NULL));

    if (argc > 1) {
	nwords = atoi(argv[1]);
    } else {
	nwords = MAXGEN;
    }
    
    for (i = 0; i < NPREF; i++) /* set up initial prefix */
	prefix[i] = NONWORD;

    build(prefix, stdin);
    add(prefix, NONWORD);
    generate(nwords);

    return 0;
}
