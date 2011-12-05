
class InvalidGroupError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'InvalidGroupError: %s' % self.msg


class NoSuchElementError(Exception):
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return 'NoSuchElementError: %s' % self.element


class FiniteGroup(object):
    def __init__(self, element_set, operation):
        self.operation = operation
        self.elements = {g: FiniteGroupElement(self, g) for g in element_set}
        self.identity = self._compute_identity()

    def __eq__(self, other):
        if not isinstance(other, FiniteGroup):
            return False
        return (self.operation == other.operation and
                self.elements.keys() == other.elements.keys())

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        elements = repr(self.elements.keys())
        return 'FiniteGroup(%s, %s)' % (elements, self.operation)

    def __str__(self):
        return str(self.elements.keys())

    def _compute_identity(self):
        identity = None
        elements = self.elements.values()
        for e in elements:
            if all(g == e * g for g in elements if g is not e):
                if identity:
                    raise InvalidGroupError('More than one identity!')
                identity = e
        return identity

    def element(self, element):
        if element not in self.elements:
            raise NoSuchElementError(element)
        return self.elements[element]


class FiniteGroupElement(object):
    def __init__(self, group, element):
        self.group = group
        self.element = element

    def __eq__(self, other):
        if not isinstance(other, FiniteGroupElement):
            return False
        return self.group == other.group and self.element == other.element

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        group = repr(self.group)
        element = repr(self.element)
        return 'FiniteGroupElement(%s, %s)' % (group, element)

    def __str__(self):
        return str(self.element)

    def __mul__(self, other):
        result = self.group.operation(self.element, other.element)
        return FiniteGroupElement(self.group, result)

    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError('must raise group element to integer power')
        res = self.group.identity
        g = self if other >= 0 else self.inverse()
        for i in xrange(abs(other)):
            res = res * g
        return res

    def inverse(self):
        if self == self.group.identity:
            return self
        for g in self.group.elements.values():
            if g * self == self.group.identity:
                return g
        raise InvalidGroupError('No inverse for element %s!' % self)

    def order(self):
        g = self
        order = 1
        while g != self.group.identity:
            g = g * self
            print g
            order += 1
        return order


# =============================================================================
# Symmetric groups
    
def subsets(x):
    if not x:
        return [[]]
    else:
        top = x[0]
        left = subsets(x[1:])
        right = [[top] + s for s in left]
        return left + right


def permutations(x):
    if not x: return [()]
    ret = []
    for first in x:
        rest = permutations([item for item in x if item is not first])
        perms = [(first,) + p for p in rest]
        ret.extend(perms)
    return ret


def compose(f, g):
    return tuple(f[x - 1] for x in g)


class SymmetricGroup(FiniteGroup):
    def __init__(self, n):
        elements = permutations(range(1, n + 1))
        operation = compose
        FiniteGroup.__init__(self, elements, operation)
