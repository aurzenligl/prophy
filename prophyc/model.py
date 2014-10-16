from collections import namedtuple
from itertools import ifilter, islice

class Kind:
    FIXED = 0
    DYNAMIC = 1
    UNLIMITED = 2

""" Model consists of 6 kinds of symbols:
Includes, Constants, Enums, Typedefs, Structs, Unions. """

Include = namedtuple("Include", ["name"])

Constant = namedtuple("Constant", ["name", "value"])

Enum = namedtuple("Enum", ["name", "members"])
EnumMember = namedtuple("EnumMember", ["name", "value"])

class Typedef(object):

    def __init__(self, name, type, **kwargs):
        self.name = name
        self.type = type
        if 'definition' in kwargs:
            self.definition = kwargs['definition']

    def __cmp__(self, other):
        return (cmp(self.name, other.name) or
                cmp(self.type, other.type))

    def __repr__(self):
        return '{0} {1}'.format(self.type, self.name)

class Struct(object):

    def __init__(self, name, members):
        self.name = name
        self.members = members

        self.kind = evaluate_struct_kind(self)
        self.byte_size = None # byte size of complete struct, dynamic/greedy arrays assumed empty
        self.alignment = None

    def __cmp__(self, other):
        return (cmp(self.name, other.name) or
                cmp(self.members, other.members))

    def __repr__(self):
        return self.name + ''.join(('\n    {}'.format(x) for x in self.members)) + '\n'

class StructMember(object):

    def __init__(self, name, type,
                 bound = None, size = None,
                 unlimited = False, optional = False,
                 definition = None):
        assert(sum((bool(bound or size), unlimited, optional)) <= 1)

        self.name = name
        self.type = type
        self.array = bool(bound or size or unlimited)
        self.bound = bound
        self.size = size
        self.optional = optional

        self.definition = definition
        self.kind = evaluate_member_kind(self) # type kind, not influenced by array or optional
        self.byte_size = None # byte size of field influenced by array: multiplied by fixed/limited size, 0 if dynamic/greedy
        self.alignment = None

    def __cmp__(self, other):
        return (cmp(self.name, other.name) or
                cmp(self.type, other.type) or
                cmp(self.array, other.array) or
                cmp(self.bound, other.bound) or
                cmp(self.size, other.size) or
                cmp(self.optional, other.optional))

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

class Union(object):

    def __init__(self, name, members):
        self.name = name
        self.members = members

        self.kind = Kind.FIXED
        self.byte_size = None
        self.alignment = None

    def __cmp__(self, other):
        return (cmp(self.name, other.name) or
                cmp(self.members, other.members))

    def __repr__(self):
        return self.name + ''.join(('\n    {}'.format(x) for x in self.members)) + '\n'

class UnionMember(object):

    def __init__(self, name, type, discriminator,
                 definition = None):
        self.name = name
        self.type = type
        self.discriminator = discriminator

        self.definition = definition
        self.kind = evaluate_member_kind(self)
        self.byte_size = None
        self.alignment = None

    def __cmp__(self, other):
        return (cmp(self.name, other.name) or
                cmp(self.type, other.type) or
                cmp(self.discriminator, other.discriminator))

    def __repr__(self):
        return '{0}: {1} {2}'.format(self.discriminator, self.type, self.name)

""" Utils """

def split_after(nodes, pred):
    part = []
    for x in nodes:
        part.append(x)
        if pred(x):
            yield part
            part = []
    if part:
        yield part

""" Following functions process model. """

def topological_sort(nodes):
    """Sorts nodes."""
    def get_include_deps(include):
        return []
    def get_constant_deps(constant):
        return filter(lambda x: not x.isdigit(),
                      reduce(lambda x, y: x.replace(y, " "), "()+-", constant.value).split())
    def get_typedef_deps(typedef):
        return [typedef.type]
    def get_enum_deps(enum):
        return []
    def get_struct_deps(struct):
        return [member.type for member in struct.members]
    def get_union_deps(union):
        return [member.type for member in union.members]
    deps_visitor = {
        Include: get_include_deps,
        Constant: get_constant_deps,
        Typedef: get_typedef_deps,
        Enum: get_enum_deps,
        Struct: get_struct_deps,
        Union: get_union_deps
    }
    def get_deps(node):
        return deps_visitor[type(node)](node)
    def model_sort_rotate(nodes, known, available, index):
        node = nodes[index]
        for dep in get_deps(node):
            if dep not in known and dep in available:
                found_index, found = next(ifilter(lambda x: x[1].name == dep,
                                          enumerate(islice(nodes, index + 1, None), start = index + 1)))
                nodes.insert(index, nodes.pop(found_index))
                return True
        known.add(node.name)
        return False
    known = set(x + y for x in "uir" for y in ["8", "16", "32", "64"])
    available = set(node.name for node in nodes)
    index = 0
    max_index = len(nodes)
    while index < max_index:
        if not model_sort_rotate(nodes, known, available, index):
            index = index + 1

def cross_reference(nodes):
    """Adds definition reference to Typedef and StructMember."""
    types = {node.name: node for node in nodes}
    def do_cross_reference(symbol):
        symbol.definition = types.get(symbol.type)
    for node in nodes:
        if isinstance(node, Typedef):
            do_cross_reference(node)
        elif isinstance(node, Struct):
            map(do_cross_reference, node.members)

def evaluate_node_kind(node):
    while isinstance(node, Typedef):
        node = node.definition
    if isinstance(node, Struct):
        return node.kind
    else:
        return Kind.FIXED
def evaluate_struct_kind(node):
    if node.members:
        if node.members[-1].greedy:
            return Kind.UNLIMITED
        elif any(x.dynamic for x in node.members):
            return Kind.DYNAMIC
        else:
            return max(x.kind for x in node.members)
    else:
        return Kind.FIXED
def evaluate_member_kind(member):
    if member.definition:
        return evaluate_node_kind(member.definition)
    else:
        return Kind.FIXED
def evaluate_kinds(nodes):
    """Adds kind to Struct and StructMember. Requires cross referenced nodes."""
    for node in nodes:
        if isinstance(node, Struct):
            for member in node.members:
                member.kind = evaluate_member_kind(member)
            node.kind = evaluate_struct_kind(node)

def partition(members):
    """Splits struct members to parts, each of which ends with dynamic field."""
    main = []
    parts = []
    current = main
    for member in members[:-1]:
        current.append(member)
        if member.kind == Kind.DYNAMIC or member.dynamic:
            current = []
            parts.append(current)
    if members:
        current.append(members[-1])
    return main, parts

builtin_byte_sizes = {
    'i8': (1, 1),
    'i16': (2, 2),
    'i32': (4, 4),
    'i64': (8, 8),
    'u8': (1, 1),
    'u16': (2, 2),
    'u32': (4, 4),
    'u64': (8, 8),
    'r32': (4, 4),
    'r64': (8, 8),
    'byte': (1, 1)
}
def evaluate_node_size(node):
    while isinstance(node, Typedef) and node.definition:
        node = node.definition
    if isinstance(node, (Struct, Union)):
        return (node.byte_size, node.alignment)
    elif isinstance(node, Enum):
        return builtin_byte_sizes['u32']
    elif node.type in builtin_byte_sizes:
        return builtin_byte_sizes[node.type]
    else:
        return (None, None) # unknown type, e.g. empty typedef
def evaluate_member_size(member):
    if member.definition:
        byte_size, alignment = evaluate_node_size(member.definition)
    elif member.type in builtin_byte_sizes:
        byte_size, alignment = builtin_byte_sizes[member.type]
    else:
        byte_size, alignment = (None, None) # unknown type
    if member.array and byte_size is not None:
        byte_size = member.size and (byte_size * int(member.size)) or 0
    if member.optional:
        alignment = max(builtin_byte_sizes['u32'][1], alignment)
        byte_size = byte_size + alignment
    return (byte_size, alignment)
def evaluate_struct_size(node):
    alignment = node.members and max(x.alignment for x in node.members) or 1
    byte_size = 0
    for member in node.members:
        byte_size += (member.alignment - byte_size % member.alignment) % member.alignment
        byte_size += member.byte_size
    byte_size += (alignment - byte_size % alignment) % alignment
    return (byte_size, alignment)
def evaluate_sizes(nodes):
    """Adds byte_size and alignment to Struct, StructMember, Union, UnionMember.
       Requires cross referenced nodes and evaluated kinds.
    """
    for node in nodes:
        if isinstance(node, (Struct, Union)):
            for member in node.members:
                member.byte_size, member.alignment = evaluate_member_size(member)
            if any(member.byte_size is None for member in node.members):
                node.byte_size, node.alignment = (None, None)
                continue
            if isinstance(node, Struct):
                parts = split_after(node.members, lambda x: (x.kind == Kind.DYNAMIC) or (x.array and not x.size))
                for part in [x for x in parts][1:]:
                    part[0].alignment = max(part[0].alignment, max(x.alignment for x in part))
                node.byte_size, node.alignment = evaluate_struct_size(node)
            elif isinstance(node, Union):
                node.byte_size = builtin_byte_sizes['u32'] + max(x.byte_size for x in node.members)
                node.alignment = max(x.alignment for x in node.members)
