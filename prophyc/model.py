from collections import namedtuple
from itertools import islice

from .six import ifilter, reduce
from . import calc

""" Exception types """
class GenerateError(Exception): pass

class ParseError(Exception):
    def __init__(self, errors):
        Exception.__init__(self, "parsing error")
        self.errors = errors
        """Collection of 2-tuples of location and message."""

""" Determines struct member wire format type. """
class Kind:
    FIXED = 0
    DYNAMIC = 1
    UNLIMITED = 2

""" Builtin types byte size and alignment. """
BUILTIN_SIZES = {
    'i8': 1,
    'i16': 2,
    'i32': 4,
    'i64': 8,
    'u8': 1,
    'u16': 2,
    'u32': 4,
    'u64': 8,
    'r32': 4,
    'r64': 8,
    'byte': 1
}

""" Union and optional discriminator byte size. """
DISC_SIZE = BUILTIN_SIZES['u32']

""" Enum byte size. """
ENUM_SIZE = BUILTIN_SIZES['u32']

""" Model consists of 6 kinds of symbols:
Includes, Constants, Enums, Typedefs, Structs, Unions. """

Include = namedtuple("Include", ["name", "nodes"])

Constant = namedtuple("Constant", ["name", "value"])

class Enum(object):

    def __init__(self, name, members):
        self.name = name
        self.members = members

    def __eq__(self, other):
        return ((self.name == other.name) and
                (self.members == other.members))

    def __repr__(self):
        return self.name + ''.join(('\n    {}'.format(x) for x in self.members)) + '\n'

class EnumMember(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return ((self.name == other.name) and
                (self.value == other.value))

    def __repr__(self):
        return '{0} {1}'.format(self.name, self.value)

class Typedef(object):

    def __init__(self, name, type_, **kwargs):
        self.name = name
        self.type_ = type_
        if 'definition' in kwargs:
            self.definition = kwargs['definition']

    def __eq__(self, other):
        return ((self.name == other.name) and
                (self.type_ == other.type_))

    def __repr__(self):
        return '{0} {1}'.format(self.type_, self.name)

class Struct(object):

    def __init__(self, name, members):
        self.name = name
        self.members = members

        self.kind = evaluate_struct_kind(self)

        self.byte_size = None
        """byte size of complete struct, dynamic/greedy arrays assumed empty"""

        self.alignment = None

    def __eq__(self, other):
        return ((self.name == other.name) and
                (self.members == other.members))

    def __repr__(self):
        return self.name + ''.join(('\n    {}'.format(x) for x in self.members)) + '\n'

class StructMember(object):

    def __init__(self, name, type_,
                 bound = None, size = None,
                 unlimited = False, optional = False,
                 definition = None):
        assert(sum((bool(bound or size), unlimited, optional)) <= 1)

        self.name = name
        self.type_ = type_
        self.array = bool(bound or size or unlimited)
        self.bound = bound
        self.size = size
        self.optional = optional

        self.definition = definition

        self.numeric_size = None
        """integral number indicating array size (it may be a string with enum member or constant name)"""

        self.kind = evaluate_member_kind(self)
        """type kind, not influenced by array or optional"""

        self.byte_size = None
        """byte size of field influenced by array: multiplied by fixed/limited size, 0 if dynamic/greedy"""

        self.alignment = None

        self.padding = None
        """amount of bytes to add before next field. If field dynamic: negative alignment of next field"""

    def __eq__(self, other):
        return ((self.name == other.name) and
                (self.type_ == other.type_) and
                (self.array == other.array) and
                (self.bound == other.bound) and
                (self.size == other.size) and
                (self.optional == other.optional))

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
        return fmt.format(self.type_, self.name, self.bound, self.size)

    @property
    def fixed(self):
        return not self.bound and self.size

    @property
    def dynamic(self):
        return self.bound and not self.size

    @property
    def limited(self):
        return self.bound and self.size

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

    def __eq__(self, other):
        return ((self.name == other.name) and
                (self.members == other.members))

    def __repr__(self):
        return self.name + ''.join(('\n    {}'.format(x) for x in self.members)) + '\n'

class UnionMember(object):

    def __init__(self, name, type_, discriminator,
                 definition = None):
        self.name = name
        self.type_ = type_
        self.discriminator = discriminator

        self.definition = definition
        self.kind = evaluate_member_kind(self)
        self.byte_size = None
        self.alignment = None

    def __eq__(self, other):
        return ((self.name == other.name) and
                (self.type_ == other.type_) and
                (self.discriminator == other.discriminator))

    def __repr__(self):
        return '{0}: {1} {2}'.format(self.discriminator, self.type_, self.name)

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
        return [typedef.type_]
    def get_enum_deps(enum):
        return [member.name for member in enum.members]
    def get_struct_deps(struct):
        return [member.type_ for member in struct.members]
    def get_union_deps(union):
        return [member.type_ for member in union.members]
    def get_deps(node):
        if isinstance(node, Include): return get_include_deps(node)
        elif isinstance(node, Constant): return get_constant_deps(node)
        elif isinstance(node, Typedef): return get_typedef_deps(node)
        elif isinstance(node, Enum): return get_enum_deps(node)
        elif isinstance(node, Struct): return get_struct_deps(node)
        elif isinstance(node, Union): return get_union_deps(node)
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

def cross_reference(nodes, warn = None):
    """
    Adds definition reference to Typedef and StructMember.
    Adds numeric_size to StructMember if it's a sized array.
    """
    def get_type_defitinions(nodes):
        included = set()
        types = {}
        def add_nodes_level(nodes):
            for node in nodes:
                if isinstance(node, Include):
                    if node.name not in included:
                        included.add(node.name)
                        add_nodes_level(node.nodes)
                else:
                    types[node.name] = node
        add_nodes_level(nodes)
        return types

    def get_constant_definitions(nodes):
        def eval_int(x, constants):
            try:
                return int(x)
            except ValueError:
                try:
                    return calc.eval(x, constants)
                except calc.ParseError:
                    return None
        included = set()
        constants = {}
        def add_constants_level(nodes):
            for node in nodes:
                if isinstance(node, Include):
                    if node.name not in included:
                        included.add(node.name)
                        add_constants_level(node.nodes)
                elif isinstance(node, Constant):
                    constants[node.name] = eval_int(node.value, constants)
                elif isinstance(node, Enum):
                    for member in node.members:
                        constants[member.name] = eval_int(member.value, constants)
        add_constants_level(nodes)
        return constants

    types = get_type_defitinions(nodes)
    constants = get_constant_definitions(nodes)

    def cross_reference_types(node):
        if node.type_ in BUILTIN_SIZES:
            node.definition = None
            return
        found = types.get(node.type_)
        if not found:
            if warn:
                warn("type '%s' not found" % node.type_)
        node.definition = found

    def evaluate_array_sizes(node):
        def to_int(x):
            try:
                return int(x)
            except ValueError:
                val = constants.get(x)
                return val is not None and val or calc.eval(x, constants)
        if node.size:
            try:
                node.numeric_size = to_int(node.size)
            except calc.ParseError as e:
                if warn:
                    warn(str(e))
                node.numeric_size = None

    for node in nodes:
        if isinstance(node, Typedef):
            cross_reference_types(node)
        elif isinstance(node, Struct):
            list(map(cross_reference_types, node.members))
            list(map(evaluate_array_sizes, node.members))
        elif isinstance(node, Union):
            list(map(cross_reference_types, node.members))

def evaluate_struct_kind(node):
    """Adds kind to Struct. Requires cross referenced nodes."""
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
    """Adds kind to StructMember. Requires cross referenced nodes."""
    def evaluate_node_kind(node):
        while isinstance(node, Typedef):
            node = node.definition
        if isinstance(node, Struct):
            return node.kind
        else:
            return Kind.FIXED
    if member.definition:
        return evaluate_node_kind(member.definition)
    else:
        return Kind.FIXED

def evaluate_kinds(nodes):
    """Adds kind to all Structs and StructMembers. Requires cross referenced nodes."""
    for node in nodes:
        if isinstance(node, Struct):
            for member in node.members:
                member.kind = evaluate_member_kind(member)
            node.kind = evaluate_struct_kind(node)

def evaluate_sizes(nodes):
    """
    Adds byte_size and alignment to Struct, StructMember, Union, UnionMember.
    Requires cross referenced nodes and evaluated kinds.
    """
    def evaluate_node_size(node):
        while isinstance(node, Typedef) and node.definition:
            node = node.definition
        if isinstance(node, (Struct, Union)):
            return (node.byte_size, node.alignment)
        elif isinstance(node, Enum):
            return (ENUM_SIZE, ENUM_SIZE)
        elif node.type_ in BUILTIN_SIZES:
            byte_size = BUILTIN_SIZES[node.type_]
            return (byte_size, byte_size)
        else:
            return (None, None) # unknown type, e.g. empty typedef

    def evaluate_array_and_optional_size(member):
        if member.array and member.byte_size is not None:
            member.byte_size = member.numeric_size and (member.byte_size * member.numeric_size) or 0
        elif member.optional:
            member.alignment = max(DISC_SIZE, member.alignment)
            member.byte_size = member.byte_size + member.alignment

    def evaluate_member_size(member):
        if isinstance(member, StructMember) and (member.size and member.numeric_size is None):
            size_alignment = (None, None) # unknown array size
        elif member.definition:
            size_alignment = evaluate_node_size(member.definition)
        elif member.type_ in BUILTIN_SIZES:
            byte_size = BUILTIN_SIZES[member.type_]
            size_alignment = (byte_size, byte_size)
        else:
            size_alignment = (None, None) # unknown type
        member.byte_size, member.alignment = size_alignment
        return size_alignment != (None, None)

    def evaluate_empty_size(node):
        node.byte_size, node.alignment = (None, None)

    def evaluate_members_sizes(node):
        if not all(list(map(evaluate_member_size, node.members))):
            evaluate_empty_size(node)
            return False
        return True

    def evaluate_partial_padding_size(node):
        parts = split_after(node.members, lambda x: (x.kind == Kind.DYNAMIC) or (x.array and not x.size))
        for part in [x for x in parts][1:]:
            part[0].alignment = max(part[0].alignment, max(x.alignment for x in part))

    def evaluate_struct_size(node):
        def is_member_dynamic(m):
            return m.dynamic or m.greedy or m.kind != Kind.FIXED
        alignment = node.members and max(x.alignment for x in node.members) or 1
        byte_size = 0
        prev_member = node.members and node.members[0] or None
        for member in node.members:
            padding = (member.alignment - byte_size % member.alignment) % member.alignment
            byte_size += member.byte_size + padding
            if is_member_dynamic(prev_member) and (prev_member.alignment < member.alignment):
                prev_member.padding = -(member.alignment)
            else:
                prev_member.padding = padding
            prev_member = member
        if node.members:
            padding = (alignment - byte_size % alignment) % alignment
            byte_size += padding
            if any(is_member_dynamic(m) for m in node.members):
                prev_member.padding = (node.members[-1].alignment < alignment) and (-alignment) or 0
            else:
                prev_member.padding = padding
        node.byte_size, node.alignment = byte_size, alignment

    def evaluate_union_size(node):
        node.alignment = max(DISC_SIZE, node.members and max(x.alignment for x in node.members) or 1)
        node.byte_size = (node.members and max(x.byte_size for x in node.members) or 0) + node.alignment
        node.byte_size = int((node.byte_size + node.alignment - 1) / node.alignment) * node.alignment

    for node in nodes:
        if isinstance(node, Struct):
            if evaluate_members_sizes(node):
                list(map(evaluate_array_and_optional_size, node.members))
                evaluate_partial_padding_size(node)
                evaluate_struct_size(node)
        elif isinstance(node, Union):
            if evaluate_members_sizes(node):
                evaluate_union_size(node)

def partition(members):
    """
    Splits struct members to parts, each of which ends with dynamic field.
    Requires cross referenced nodes and evaluated kinds.
    """
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
