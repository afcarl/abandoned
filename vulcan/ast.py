class ProgramNode(object):
    def __init__(self, stats):
        self.stats = stats

    def __repr__(self):
        return repr(self.stats)

class ReturnStatNode(object):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return 'return(%s)' % self.expr

class DeclNode(object):
    def __init__(self, ident, expr):
        self.ident = ident
        self.expr = expr

    def __repr__(self):
        return 'decl(%s, %s)' % (self.ident, self.expr)

class AssignNode(object):
    def __init__(self, ident, expr):
        self.ident = ident
        self.expr = expr

    def __repr__(self):
        return 'assign(%s, %s)' % (self.ident, self.expr)

class WhileLoopNode(object):
    def __init__(self, test, body):
        self.test = test
        self.body = body

    def __repr__(self):
        return 'while(%s, %s)' % (self.test, self.body)

class IfNode(object):
    def __init__(self, test, body, elif_nodes, else_node):
        self.test = test
        self.body = body
        self.elif_nodes = elif_nodes
        self.else_node = else_node

    def __repr__(self):
        args = (self.test, self.body, self.elif_nodes, self.else_node)
        return 'if(%s, %s, %s, %s)' % args

class ElifNode(object):
    def __init__(self, test, body):
        self.test = test
        self.body = body

    def __repr__(self):
        return 'elif(%s, %s)' % (self.test, self.body)

class ElseNode(object):
    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return 'else(%s)' % self.body

class FuncDefNode(object):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return 'func_def(%s, %s, %s)' % (self.name, self.params, self.body)

class BlockNode(object):
    def __init__(self, stats):
        self.stats = stats

    def __repr__(self):
        return 'block(%s)' % self.stats

class ExprListNode(object):
    def __init__(self, exprs):
        self.exprs = exprs

    def __repr__(self):
        return 'expr_list(%s)' % self.exprs

class IdentNode(object):
    def __init__(self, ident):
        self.ident = ident

    def __repr__(self):
        return repr(self.ident)

class NumNode(object):
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return repr(self.num)

class FuncCallNode(object):
    def __init__(self, ident, args):
        self.ident = ident
        self.args = args

    def __repr__(self):
        return '%s(%s)' % (self.ident, self.args)

class UnaryOpNode(object):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return '%s(%s)' % (self.op, self.expr)

class BinaryOpNode(object):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return '%s(%s, %s)' % (self.op, self.left, self.right)
