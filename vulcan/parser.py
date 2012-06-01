import lexer
from lexer import EOF, IDENT, NUM, DEF, IF, ELIF, ELSE, WHILE, END, AND, OR, NOT, RETURN, LPAREN, RPAREN, DECL, ASSIGN, EQ, LT, LTE, GT, GTE, ADD, SUB, MUL, QUO, REM, COMMA

# ----------------------------------------------------------------------------
# Exceptions

class SyntaxError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'Syntax error: %s' % self.msg


# -----------------------------------------------------------------------------
# Parse tree

class Node(object):
    def __init__(self, production, children=None):
        self.production = production
        self.children = children or []

    def __repr__(self):
        return 'Node(%s, %s)' % (self.production.__name__, self.children)


# ----------------------------------------------------------------------------
# Parsing

class Parser(object):

    """An LL(2) recursive-descent parser for the Vulcan language."""

    def __init__(self, lexer):
        self.lexer = lexer
        la1 = self.lexer.next()
        la2 = self.lexer.next()
        self.lookahead = (la1, la2)

    def _eat(self):
        tok = self.lexer.next()
        la1, la2 = self.lookahead
        self.lookahead = (la2, tok)
        return la1

    def _la(self, n):
        return self.lookahead[n-1]

    def _match(self, exp_type):
        t = self._la(1)
        if t.tt == exp_type:
            return self._eat()
        raise lexer.ExpectedTokenError(exp_type, t.tt, t.pos, t.line)

    # program: block
    def program(self):
        return Node(self.program, [self.block()])

    def _is_stat(self):
        tt1, tt2 = self._la(1).tt, self._la(2).tt
        if tt1 in (DEF, IF, WHILE, RETURN):
            return True
        if tt1 == IDENT and tt2 in (ASSIGN, DECL):
            return True
        if self._is_expr():
            return True
        return False

    # stat
    #     : func_def
    #     | if_stat
    #     | while_loop
    #     | assign_stat
    #     | decl_stat
    #     | return_stat
    #     | expr
    #     ;
    def stat(self):
        tt1, tt2 = self._la(1).tt, self._la(2).tt
        if tt1 == DEF:
            return Node(self.stat, [self.func_def()])
        if tt1 == IF:
            return Node(self.stat, [self.if_stat()])
        if tt1 == WHILE:
            return Node(self.stat, [self.while_loop()])
        if tt1 == IDENT and tt2 == ASSIGN:
            return Node(self.stat, [self.assign_stat()])
        if tt1 == IDENT and tt2 == DECL:
            return Node(self.stat, [self.decl_stat()])
        if tt1 == RETURN:
            return Node(self.stat, [self.return_stat()])
        if self._is_expr():
            return Node(self.stat, [self.expr()])
        raise SyntaxError('unknown stat: %s' % tt1)

    # ident_list
    #     :
    #     | IDENT (COMMA IDENT)*
    #     ;
    def ident_list(self):
        idents = []
        if self._la(1).tt != IDENT:
            return Node(self.ident_list, idents)
        idents.append(self._eat().contents)
        while self._la(1).tt == COMMA:
            self._match(COMMA)
            idents.append(self._eat().contents)
        return Node(self.ident_list, idents)

    # func_def: DEF IDENT LPAREN ident_list RPAREN block END
    def func_def(self):
        self._match(DEF)
        name = self._match(IDENT)
        self._match(LPAREN)
        params = self.ident_list()
        self._match(RPAREN)
        body = self.block()
        self._match(END)
        return Node(self.func_def, [name, params, body])

    # block: stat*
    def block(self):
        stats = []
        while self._is_stat():
            stats.append(self.stat())
        return Node(self.block, stats)

    # elif_clause: ELIF expr block
    def elif_clause(self):
        self._match(ELIF)
        test = self.expr()
        body = self.block()
        return Node(self.elif_clause, [test, body])

    # else_clause: ELSE block
    def else_clause(self):
        self._match(ELSE)
        body = self.block()
        return Node(self.else_clause, [body])

    # if_stat: IF expr block elif_clause* (ELSE expr block)? END
    def if_stat(self):
        self._match(IF)
        test = self.expr()
        body = self.block()

        elifs = []
        while self._la(1).tt == ELIF:
            elifs.append(self.elif_clause())

        else_node = None
        if self._la(1).tt == ELSE:
            else_node = self.else_clause()

        self._match(END)
        return Node(self.if_stat, [test, body] + elifs + [else_node])

    # while_loop: WHILE expr block END
    def while_loop(self):
        self._match(WHILE)
        test = self.expr()
        body = self.block()
        self._match(END)
        return Node(self.while_loop, [test, body])

    # assign_stat: IDENT ASSIGN expr
    def assign_stat(self):
        name = self._match(IDENT)
        self._match(ASSIGN)
        val = self.expr()
        return Node(self.assign_stat, [name, val])

    # decl_stat: IDENT DECL expr
    def decl_stat(self):
        name = self._match(IDENT)
        self._match(DECL)
        val = self.expr()
        return Node(self.decl_stat, [name, val])

    # return_stat: return expr
    def return_stat(self):
        self._match(RETURN)
        return Node(self.return_stat, [self.expr()])

    # func_call : IDENT LPAREN expr_list RPAREN
    def func_call(self):
        name = self._match(IDENT)
        self._match(LPAREN)
        args = self.expr_list()
        self._match(RPAREN)
        return Node(self.func_call, [name, args])

    def _is_expr(self):
        return self._la(1).tt in (IDENT, NUM, LPAREN, ADD, SUB, NOT)

    # expr: or_expr
    def expr(self):
        return Node(self.expr, [self.or_expr()])
    
    # or_expr: and_expr (OR and_expr)*
    def or_expr(self):
        exprs = [self.and_expr()]
        while self._la(1).tt == OR:
            self._match(OR)
            exprs.append(self.and_expr())
        return Node(self.or_expr, exprs)

    # and_expr: comparison_expr (AND comparison_expr)*
    def and_expr(self):
        exprs = [self.comparison_expr()]
        while self._la(1).tt == AND:
            self._match(AND)
            exprs.append(self.comparison_expr())
        return Node(self.and_expr, exprs)

    # comparison_expr: arithmetic_expr ((EQ|LT|LTE|GT|GTE) arithmetic_expr)*
    def comparison_expr(self):
        children = [self.arithmetic_expr()]
        while self._la(1).tt in (EQ, LT, LTE, GT, GTE):
            children.append(self._eat())
            children.append(self.arithmetic_expr())
        return Node(self.comparison_expr, children)

    # arithmetic_expr: term ((ADD|SUB) term)*
    def arithmetic_expr(self):
        children = [self.term()]
        while self._la(1).tt in (ADD, SUB):
            children.append(self._eat())
            children.append(self.term())
        return Node(self.arithmetic_expr, children)

    # term: factor ((MUL|QUO|REM) factor)*
    def term(self):
        children = [self.factor()]
        while self._la(1).tt in (MUL, QUO, REM):
            children.append(self._eat())
            children.append(self.factor())
        return Node(self.term, children)

    # factor:
    #     : func_call
    #     | IDENT
    #     | NUM
    #     | LPAREN expr RPAREN
    #     | (ADD|SUB|NOT) factor
    #     ;
    def factor(self):
        tt1, tt2 = self._la(1).tt, self._la(2).tt
        if tt1 == IDENT and tt2 == LPAREN:
            return Node(self.factor, [self.func_call()])
        if tt1 == IDENT:
            return Node(self.factor, [self._eat()])
        if tt1 == NUM:
            return Node(self.factor, [self._eat()])
        if tt1 == LPAREN:
            lp = self._match(LPAREN)
            expr = self.expr()
            self._match(RPAREN)
            return Node(self.factor, [expr])
        if tt1 in (ADD, SUB, NOT):
            op = self._eat()
            expr = self.factor()
            return Node(self.factor, [op, expr])
        raise SyntaxError('unknown factor: %s' % tt1)
        
    # expr_list
    #     : 
    #     | expr (COMMA expr)*
    #     ;
    def expr_list(self):
        if not self._is_expr():
            return Node(expr_list)
        exprs = [self.expr()]
        while self._la(1).tt == COMMA:
            self._match(COMMA)
            exprs.append(self.expr())
        return Node(self.expr_list, exprs)


# ----------------------------------------------------------------------------
# Convenience functions

def parse(text):
    """Builds and returns a parse tree from the given program string."""
    if not text:
        return None
    return Parser(lexer.Lexer(text)).program()


# ----------------------------------------------------------------------------
# Running from the command line

import sys


def main(args):
    if args:
        for filename in args:
            with open(filename) as f:
                print parse(f.read())
    else:
        print parse(sys.stdin.read())


if __name__ == '__main__':
    main(sys.argv[1:])

