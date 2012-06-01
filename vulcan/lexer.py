# -----------------------------------------------------------------------------
# Exceptions

class ExpectedTokenError(Exception):
    def __init__(self, exp, actual, pos, line):
        self.exp = exp
        self.actual = actual
        self.line = line
        self.pos = pos

    def __str__(self):
        args = (self.exp, self.pos, self.line, self.actual)
        return 'Expected token %s at position %d on line %d, got %s' % args


class UnknownTokenError(Exception):
    def __init__(self, ch, pos, line):
        self.ch = ch
        self.line = line
        self.pos = pos

    def __str__(self):
        args = (self.pos, self.line, self.ch)
        return 'Unknown token lookahead at position %d on line %d: %s' % args


# -----------------------------------------------------------------------------    
# Lexical tokens

EOF = 'EOF'

IDENT = 'ident'
NUM = 'num'

DEF = 'def'
IF = 'if'
ELIF = 'elif'
ELSE = 'else'
WHILE = 'while'
END = 'end'
AND = 'and'
OR = 'or'
NOT = 'not'
RETURN = 'return'

LPAREN = '('
RPAREN = ')'
DECL = ':='
ASSIGN = '='
EQ = '=='
LT = '<'
LTE = '<='
GT = '>'
GTE = '>='
ADD = '+'
SUB = '-'
MUL = '*'
QUO = '/'
REM = '%'
COMMA = ','


class Token(object):

    """A lexical token in the Vulcan language."""
    
    def __init__(self, tt, contents, pos, line):
        self.tt = tt
        self.contents = contents
        self.pos = pos
        self.line = line

    def __repr__(self):
        return ('Token(%s, %s, %d, %d)' %
                (self.tt, self.contents, self.pos, self.line))

    def __str__(self):
        return ('<%s, %s, %d, %d>' %
                (self.tt, self.contents, self.pos, self.line))


# -----------------------------------------------------------------------------
# Tokenzing

whitespace = ' \t\n'
letters = 'abcdefghijklmnopqrstuvwxyz'
upper = letters.upper()
digits = '0123456789'
single_symbols = '()+-*/%,'
symbols = single_symbols + ':=<>'
keywords = (DEF, IF, ELIF, ELSE, WHILE, END, AND, OR, NOT, RETURN)


class Lexer(object):
    
    """A recursive-descent lexer for the Vulcan language."""

    def __init__(self, text):
        self.pos = 0
        self.line = 0
        self.text = text
        self.ch = text[self.pos]

    def _eat(self):
        self.pos += 1
        ch = self.ch
        self.ch = self.text[self.pos] if self.pos < len(self.text) else EOF
        return ch

    def _match(self, exp):
        if self.ch == exp:
            return self._eat()
        raise ExpectedTokenError(exp, self.ch, self.pos, self.line)

    def empty(self):
        return self.ch == EOF

    def next(self):
        """Returns the next token as a tuple (type, contents, pos, line)."""
        while self.ch != EOF:
            if self.ch in whitespace:
                self.whitespace()
            elif self.ch in letters or self.ch in upper or self.ch == '_':
                return self.ident_or_keyword()
            elif self.ch in digits:
                return self.num()
            elif self.ch in symbols:
                return self.operator()
            else:
                raise UnknownTokenError(self.ch, self.pos, self.line)
        return Token(EOF, EOF, self.pos, self.line)

    # IDENT: [a-zA-Z_][a-zA-Z0-9_]*
    def ident_or_keyword(self):
        name = self._eat()
        while self.ch in letters + upper + digits or self.ch == '_':
            name += self._eat()
        if name in keywords:
            return Token(name, name, self.pos, self.line)
        return Token(IDENT, name, self.pos, self.line)

    def num(self):
        raw = self._eat()
        while self.ch in digits or self.ch == '.':
            raw += self._eat()
        return Token(NUM, float(raw), self.pos, self.line)

    def operator(self):
        if self.ch in single_symbols:
            ch = self._match(self.ch)
            return Token(ch, ch, self.pos, self.line)
        if self.ch == '=':
            self._match('=')
            if self.ch == '=':
                self._match('=')
                return Token(EQ, EQ, self.pos, self.line)
            return Token(ASSIGN, ASSIGN, self.pos, self.line)
        if self.ch == '<':
            self._match('<')
            if self.ch == '=':
                self._match('=')
                return Token(LTE, LTE, self.pos, self.line)
            return Token(LT, LT, self.pos, self.line)
        if self.ch == '>':
            self._match('>')
            if self.ch == '=':
                self._match('=')
                return Token(GTE, GTE, self.pos, self.line)
            return Token(GT, GT, self.pos, self.line)
        if self.ch == ':':
            self._match(':')
            self._match('=')
            return Token(DECL, DECL, self.pos, self.line)

    def whitespace(self):
        while self.ch in whitespace:
            if self.ch == '\n':
                self.line += 1
            self._eat()


# -----------------------------------------------------------------------------
# Convenience functions

def tokens(src):
    lex = Lexer(src)
    while not lex.empty():
        yield lex.next()


# -----------------------------------------------------------------------------
# Command-line invocation

import sys


def main(args):
    if args:
        for filename in args:
            with open(filename) as f:
                for tok in tokens(f.read()):
                    print tok
    else:
        for tok in tokens(sys.stdin.read()):
            print tok


if __name__ == '__main__':
    main(sys.argv[1:])
