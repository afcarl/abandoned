package main

import (
	"fmt"
	"io"
	"math/rand"
	"os"
	"strconv"
	"time"
)

const (
	PREFIX_LEN = 2     // Markov chain prefix length
	MAX_WORDS  = 10000 // default number of words to generate
	NONWORD    = "\n"  // can't appear as a word in the input
)

var nwords = MAX_WORDS

type prefix [PREFIX_LEN]string

// emptyPrefix returns a prefix that can't appear in the input.
func emptyPrefix() prefix {
	pref := [PREFIX_LEN]string{}
	for i := 0; i < PREFIX_LEN; i++ {
		pref[i] = NONWORD
	}
	return pref
}

// newPrefix makes a new prefix from the given words.
func newPrefix(words ...string) prefix {
	pref := [PREFIX_LEN]string{}
	for i, word := range words {
		pref[i] = word
	}
	return pref
}

// addSuffix adds a word to the suffix list for pref.
func addSuffix(states map[prefix][]string, pref prefix, suf string) {
	if suffixes, ok := states[pref]; !ok {
		states[pref] = []string{suf}
	} else {
		states[pref] = append(suffixes, suf)
	}
}

// train builds a markov chain table from the text in r.
func train(r io.Reader) map[prefix][]string {
	states := make(map[prefix][]string)
	pref := emptyPrefix()
	var w string
	for n, _ := fmt.Fscan(r, &w); n > 0; n, _ = fmt.Fscan(r, &w) {
		addSuffix(states, pref, w)
		pref = newPrefix(append(pref[1:], w)...)
	}
	addSuffix(states, pref, NONWORD)
	return states
}

// generate writes nwords of text to w using the markov chain table states.
func generate(w io.Writer, states map[prefix][]string, nwords int) {
	pref := emptyPrefix()
	for i := 0; i < nwords; i++ {
		choices := states[pref]
		word := choices[rand.Intn(len(choices))]
		io.WriteString(w, fmt.Sprintf("%s ", word))
		pref = newPrefix(append(pref[1:], word)...)
	}
	io.WriteString(w, "\n")
}

func main() {
	rand.Seed(time.Now().Unix())

	if len(os.Args) > 1 {
		num, err := strconv.Atoi(os.Args[1])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Invalid number of words: %v", os.Args[1])
			return
		}
		nwords = num
	}

	states := train(os.Stdin)
	generate(os.Stdout, states, nwords)
}
