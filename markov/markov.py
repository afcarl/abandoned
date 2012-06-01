#!/usr/bin/env python

import random
import sys

PREFIX_LEN = 2 # Markov chain prefix length
MAX_WORDS = 10000 # Default number of words to generate
NONWORD = '\n' # Can't appear as a word in the text

# train: read text from file f and build a markov prefix table
def train(f):
    states = {}
    prefix = (NONWORD,) * PREFIX_LEN
    for word in words(f):
        states.setdefault(prefix, []).append(word)
        prefix = prefix[1:] + (word,)
    states.setdefault(prefix, []).append(NONWORD)
    return states

# words: generate whitespace-delimited words from file f
def words(f):
    for line in f:
        for word in line.split():
            yield word

# generate: generate nwords of text using prefix table states
def generate(states, nwords):
    prefix = (NONWORD,) * PREFIX_LEN
    for i in xrange(nwords):
        word = random.choice(states[prefix])
        prefix = prefix[1:] + (word,)
        print word,
    
def main(args):
    nwords = int(args[0]) if args else MAX_WORDS
    states = train(sys.stdin)
    generate(states, nwords)

if __name__ == '__main__':
    main(sys.argv[1:])
