from collections import namedtuple

class Kind:
    FIXED = 0
    DYNAMIC = 1
    UNLIMITED = 2

""" Model consists of 5 kinds of symbols: Includes, Constants, Enums, Structs, Unions. """

Include = namedtuple("Include", ["name"])

Constant = namedtuple("Constant", ["name", "value"])

Enum = namedtuple("Enum", ["name", "members"])
EnumMember = namedtuple("EnumMember", ["name", "value"])

class Typedef(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.definition = None

    def __cmp__(self, other):
        return cmp(other.__dict__, self.__dict__)

    def __repr__(self):
        return '{0} {1}'.format(self.type, self.name)

class Struct(object):

    def __init__(self, name, members):
        self.name = name
        self.members = members
        self.kind = None

    def __cmp__(self, other):
        return cmp(other.__dict__, self.__dict__)

    def __repr__(self):
        return self.name + ''.join(('\n    {}'.format(x) for x in self.members)) + '\n'

class StructMember(object):

    def __init__(self, name, type,
                 bound = None, size = None,
                 unlimited = False, optional = False):
        assert(sum((bool(bound or size), unlimited, optional)) <= 1)

        self.name = name
        self.type = type
        self.array = bool(bound or size or unlimited)
        self.bound = bound
        self.size = size
        self.optional = optional
        self.definition = None
        self.kind = None

    def __cmp__(self, other):
        return cmp(other.__dict__, self.__dict__)

    def __repr__(self):
        fmts = {
            (False, False, False, False): '{0} {1}',
            (True, False, True, False): '{0} {1}[{3}]',
            (True, True, False, False): '{0} {1}<>({2})',
            (True, True, True, False): '{0} {1}<{3}>({2})',
            (True, False, False, False): '{0} {1}<...>',
            (False, False, False, True): '{0}* {1}'
        }
        fmt = fmts[(self.array, bool(self.bound), bool(self.size), self.optional)]
        return fmt.format(self.type, self.name, self.bound, self.size)

    @property
    def dynamic(self):
        return self.bound and not self.size

    @property
    def greedy(self):
        return self.array and not self.bound and not self.size

Union = namedtuple("Union", ["name", "members"])
UnionMember = namedtuple("UnionMember", ["name", "type", "discriminator"])

""" Following functions process model. """

def cross_reference(nodes):
    types = {node.name: node for node in nodes}
    def do_cross_reference(symbol):
        symbol.definition = types.get(symbol.type)
    for node in nodes:
        if isinstance(node, Typedef):
            do_cross_reference(node)
        elif isinstance(node, Struct):
            map(do_cross_reference, node.members)

def evaluate_kinds(nodes):
    """ Prerequisite to calculate kinds is to cross reference nodes. """
    def evaluate_node_kind(node):
        if isinstance(node, Typedef):
            while isinstance(node, Typedef):
                node = node.definition
            return evaluate_node_kind(node)
        elif isinstance(node, Struct):
            return node.kind
        else:
            return Kind.FIXED
    def evaluate_member_kind(member):
        if member.greedy:
            return Kind.UNLIMITED
        elif member.dynamic:
            return Kind.DYNAMIC
        elif member.definition is None:
            return Kind.FIXED
        else:
            return evaluate_node_kind(member.definition)
    for node in nodes:
        if isinstance(node, Struct):
            for member in node.members:
                member.kind = evaluate_member_kind(member)
            if node.members:
                node.kind = max(x.kind for x in node.members)
            else:
                node.kind = Kind.FIXED
