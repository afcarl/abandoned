import ast

def fold_constants(tree):
    return tree

def check_types(tree):
    return tree

from parser import parse
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            print optimize(parse(f.read()))
    else:
        try:
            while True:
                print parse(raw_input('>> '))
        except EOFError:
            pass
