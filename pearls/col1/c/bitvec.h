#ifndef BITVEC
#define BITVEC

/* bitvec_create: allocate enough unsigneds to store n bits. */
unsigned *bitvec_create(int n);

/* bitvec_set: turn on the ith bit of the bitvector vec */
void bitvec_set(unsigned *vec, int i);

/* bitvec_unset: turn off the ith bit of the bitvector vec */
void bitvec_unset(unsigned *vec, int i);

/* bitvec_get: return the ith bit of the bitvector vec */
unsigned bitvec_get(unsigned *vec, int i);

#endif
