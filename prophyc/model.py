from itertools import islice

from . import calc
from .six import ifilter, reduce, string_types

""" Exception types """


class ParseError(Exception):
    def __init__(self, errors):
        Exception.__init__(self, "parsing error")
        self.errors = errors
        """Collection of 2-tuples of location and message."""


class Kind:
    """ Determines struct member wire format type (bytes stiffness). """
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


class ModelNode(object):
    __slots__ = ("name", "_value", "docstring")
    _str_pattern = ""

    def __init__(self, name, value, docstring=""):
        assert isinstance(name, string_types), "Got name %s, expected string." % type(name).__name__
        assert isinstance(docstring, string_types), "Got doc string as %s, expected string." % type(docstring).__name__
        self.name = name
        self._value = value
        self.docstring = docstring

    @property
    def value(self):
        return self._value

    def __str__(self):
        return self._str_pattern.format(s=self)

    def __repr__(self):
        cls_name = self.__class__.__name__
        pattern = '{cls_name}({s.name!r}, {s._value!r}, {s.docstring!r})'
        return pattern.format(s=self, cls_name=cls_name)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self._value == other._value
        if isinstance(other, tuple) and len(other) in (2, 3):
            return self.name == other[0] and self._value == other[1]

    def __ne__(self, other):
        return not (self.__eq__(self, other))


class Include(ModelNode):
    _str_pattern = "include {s.name} {{\n{s._str_nodes}}};\n"
    __slots__ = ()

    def __init__(self, name, nodes, docstring=""):
        super(Include, self).__init__(name, nodes, docstring)

    @property
    def _str_nodes(self):
        return "".join("    {};\n".format(m) for m in self.nodes)

    @property
    def nodes(self):
        return self._value


class Constant(ModelNode):
    _str_pattern = "const {s.name} = {s.value!r};"
    __slots__ = ()

    def eval_int(self, all_constants):
        try:
            return int(self.value)
        except ValueError:
            try:
                return calc.eval(self.value, all_constants)
            except calc.ParseError:
                return None


class EnumMember(Constant):
    _str_pattern = "{s.name} = {s.value!r}"
    __slots__ = ()


class _Serializable(ModelNode):
    __slots__ = ("kind", "byte_size", "alignment")

    def __init__(self, name, value, docstring=""):
        super(_Serializable, self).__init__(name, value, docstring=docstring)
        self.alignment = None
        """byte size of field influenced by array: multiplied by fixed/limited size, 0 if dynamic/greedy"""
        self.byte_size = None
        """type kind, not influenced by array or optional"""
        self.calc_wire_stiffness()

    @classmethod
    def calc_wire_stiffness(cls):
        raise NotImplementedError("Abstract method to be overriden in %s" % cls.__name__)


class Typedef(_Serializable):
    _str_pattern = "typedef {s.type_} {s.name};"
    __slots__ = ("definition",)

    def __init__(self, name, node_typedef, definition=None, docstring=""):
        assert isinstance(node_typedef, string_types), "Got typedef %s, expected string." % type(node_typedef).__name__
        self.definition = definition
        super(Typedef, self).__init__(name, node_typedef, docstring=docstring)

    def __repr__(self):
        cls_name = self.__class__.__name__
        if self.docstring:
            pattern = '{cls_name}({s.name!r}, {s.type_!r}, {s.definition!r}, {s.docstring!r})'
        else:
            pattern = '{cls_name}({s.name!r}, {s.type_!r}, {s.definition!r})'
        return pattern.format(s=self, cls_name=cls_name)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return super(Typedef, self).__eq__(other) and self.definition == other.definition

    @property
    def type_(self):
        return self._value

    @type_.setter
    def type_(self, new_value):
        assert isinstance(new_value, str), "Type name is expected in string, got {}".format(type(new_value).__name__)
        self._value = new_value

    def calc_wire_stiffness(self):
        """ Typedef propagates stiffness kinds of its lowermost type """
        self.kind = Kind.FIXED
        if self.definition:
            lowermost_typedef = self.definition
            while isinstance(lowermost_typedef, Typedef):
                lowermost_typedef = lowermost_typedef.definition
            if isinstance(lowermost_typedef, Struct):
                self.kind = lowermost_typedef.kind


class StructMember(Typedef):
    __slots__ = ("array", "bound", "size", "optional", "numeric_size", "padding")

    def __init__(self, name, type_, definition=None, docstring="", bound=None, size=None, unlimited=False,
                 optional=False):
        assert sum((bool(bound or size), unlimited, optional)) <= 1, "Overconstraint"

        super(StructMember, self).__init__(name, type_, definition=definition, docstring=docstring)
        self.array = bool(bound or size or unlimited)
        self.bound = bound
        self.size = size
        self.optional = optional
        """integral number indicating array size (it may be a string with enum member or constant name)"""
        self.numeric_size = None
        """amount of bytes to add before next field. If field dynamic: negative alignment of next field"""
        self.padding = None

    @property
    def _unlimited_(self):
        "just to make __repr__ working"
        return self.array and not self.bound and not self.size

    def __repr__(self):
        cls_name = self.__class__.__name__
        pattern = '{cls_name}({s.name!r}, {s.type_!r}, {s.definition!r}, {s.docstring!r}, bound={s.bound}, size={s.size}, \
unlimited={s._unlimited_}, optional={s.optional})'
        return pattern.format(s=self, cls_name=cls_name)

    def __eq__(self, other):
        return ((self.name == other.name) and
                (self.type_ == other.type_) and
                (self.array == other.array) and
                (self.bound == other.bound) and
                (self.size == other.size) and
                (self.optional == other.optional))

    def __str__(self):
        fmts = {
            (False, False, False, False): '{0} {1}',
            (True, False, True, False): '{0} {1}[{3}]',
            (True, True, False, False): '{0} {1}<@{2}>',
            (True, True, True, False): '{0} {1}<{3}>({2})',
            (True, False, False, False): '{0} {1}<...>',
            (False, False, False, True): '{0}* {1}'
        }
        select = tuple(bool(k) for k in (self.array, self.bound, self.size, self.optional))
        return fmts[select].format(self.type_, self.name, self.bound, self.size)

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


class UnionMember(Typedef):
    _str_pattern = '{s.discriminator}: {s.type_} {s.name}'
    __slots__ = ("discriminator",)

    def __init__(self, name, type_, discriminator, definition=None, docstring=""):
        super(UnionMember, self).__init__(name, type_, definition=definition, docstring=docstring)
        self.discriminator = discriminator

    def __repr__(self):
        cls_name = self.__class__.__name__
        if self.docstring:
            pattern = '{cls_name}({s.name!r}, {s.type_!r}, {s.discriminator!r}, {s.definition!r}, {s.docstring!r})'
        else:
            pattern = '{cls_name}({s.name!r}, {s.type_!r}, {s.discriminator!r}, {s.definition!r})'

        return pattern.format(s=self, cls_name=cls_name)

    def __eq__(self, other):
        return ((self.name == other.name) and
                (self.type_ == other.type_) and
                (self.discriminator == other.discriminator))


""" Composite kinds """


class Enum(ModelNode):
    _str_pattern = "{s._collection_kind} {s.name} {{\n{s._str_members}}};\n"
    _collection_kind = "enum"
    __slots__ = ()

    @property
    def members(self):
        return self._value

    @property
    def _str_members(self):
        return "".join("    {};\n".format(m) for m in self.members)

    def check_for_duplicates(self):
        values = set()
        for m in self.members:
            if m.value in values:
                raise ValueError("Duplicate Enum value in '{}', value '{}'.".format(self.name, m.value))
            values.add(m.value)


class _SerializableContainer(_Serializable):
    """ Base for Struct and Union. Provides membership properties. """
    _str_pattern = "{s._collection_kind} {s.name} {{\n{s._str_members}}};\n"
    _collection_kind = None
    __slots__ = ()

    @property
    def members(self):
        return self._value

    @property
    def value(self):
        raise AttributeError("{} is not allowed to use .value property".format(self.__class__.__name__))

    @property
    def _str_members(self):
        return "".join("    {};\n".format(m) for m in self.members)

    def calc_wire_stiffness(self):
        """ Evaluate stiffness of the node. """
        self.kind = Kind.FIXED
        if isinstance(self, Struct):
            if self.members:
                for member in self.members:
                    member.calc_wire_stiffness()

                if self.members[-1].greedy:
                    self.kind = Kind.UNLIMITED
                elif any(x.dynamic for x in self.members):
                    self.kind = Kind.DYNAMIC
                else:
                    self.kind = max(x.kind for x in self.members)


class Struct(_SerializableContainer):
    _collection_kind = "struct"
    __slots__ = ()


class Union(_SerializableContainer):
    _collection_kind = "union"
    __slots__ = ()


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


def null_warn(_):
    pass


""" Following functions process model. """


def topological_sort(nodes):
    """Sorts nodes."""

    def get_include_deps(_):
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
        if isinstance(node, Include):
            return get_include_deps(node)
        elif isinstance(node, Constant):
            return get_constant_deps(node)
        elif isinstance(node, Typedef):
            return get_typedef_deps(node)
        elif isinstance(node, Enum):
            return get_enum_deps(node)
        elif isinstance(node, Struct):
            return get_struct_deps(node)
        elif isinstance(node, Union):
            return get_union_deps(node)

    def model_sort_rotate():
        node = nodes[index]
        for dep in get_deps(node):
            if dep not in known and dep in available:
                found_index, _ = next(ifilter(lambda x: x[1].name == dep,
                                              enumerate(islice(nodes, index + 1, None), start=index + 1)))
                nodes.insert(index, nodes.pop(found_index))
                return True
        known.add(node.name)
        return False

    known = set(x + y for x in "uir" for y in ["8", "16", "32", "64"])
    available = set(node.name for node in nodes)
    index = 0
    max_index = len(nodes)
    while index < max_index:
        if not model_sort_rotate():
            index = index + 1


def cross_reference(nodes, warn=null_warn):
    """
    Adds definition reference to Typedef and StructMember.
    Adds numeric_size to StructMember if it's a sized array.
    """

    types = {}

    def add_nodes_level(nodes_):
        included = set()
        for node_ in nodes_:
            if isinstance(node_, Include):
                if node_.name not in included:
                    included.add(node_.name)
                    add_nodes_level(node_.nodes)
            else:
                types[node_.name] = node_

    add_nodes_level(nodes)

    constants = {}

    def add_constants_level(nodes_):
        included = set()
        for node_ in nodes_:
            if isinstance(node_, Include):
                if node_.name not in included:
                    included.add(node_.name)
                    add_constants_level(node_.nodes)
            elif isinstance(node_, Constant):
                constants[node_.name] = node_.eval_int(constants)
            elif isinstance(node_, Enum):
                for member in node_.members:
                    constants[member.name] = member.eval_int(constants)

    add_constants_level(nodes)

    def cross_reference_types(node_):
        if node_.type_ in BUILTIN_SIZES:
            node_.definition = None
            return
        found = types.get(node_.type_)
        if not found:
            warn("type '%s' not found" % node_.type_)
        node_.definition = found

    def evaluate_array_sizes(node_):
        def to_int(x):
            try:
                return int(x)
            except ValueError:
                val = constants.get(x)
                return val is not None and val or calc.eval(x, constants)

        if node_.size:
            try:
                node_.numeric_size = to_int(node_.size)
            except calc.ParseError as e:
                warn(str(e))
                node_.numeric_size = None

    for node in nodes:
        if isinstance(node, Typedef):
            cross_reference_types(node)
        elif isinstance(node, Struct):
            list(map(cross_reference_types, node.members))
            list(map(evaluate_array_sizes, node.members))
        elif isinstance(node, Union):
            list(map(cross_reference_types, node.members))


def evaluate_stiffness_kinds(nodes):
    """Adds kind to all Structs and StructMembers. Requires cross referenced nodes."""
    for node in nodes:
        if isinstance(node, Struct):
            node.calc_wire_stiffness()


def evaluate_sizes(nodes, warn=null_warn):
    """
    Adds byte_size and alignment to Struct, StructMember, Union, UnionMember.
    Requires cross referenced nodes and evaluated kinds.
    """

    def evaluate_node_size(node_, parent, member):
        while isinstance(node_, Typedef) and node_.definition:
            node_ = node_.definition
        if isinstance(node_, (Struct, Union)):
            return node_.byte_size, node_.alignment
        elif isinstance(node_, Enum):
            return ENUM_SIZE, ENUM_SIZE
        elif node_.type_ in BUILTIN_SIZES:
            byte_size = BUILTIN_SIZES[node_.type_]
            return byte_size, byte_size
        else:
            # unknown type, e.g. empty typedef
            warn('%s::%s has unknown type "%s"' % (parent.name, member.name, node_.type_))
            return None, None

    def evaluate_array_and_optional_size(member):
        if member.array and member.byte_size is not None:
            member.byte_size = member.numeric_size and (member.byte_size * member.numeric_size) or 0
        elif member.optional:
            member.alignment = max(DISC_SIZE, member.alignment)
            member.byte_size = member.byte_size + member.alignment

    def evaluate_member_size(node_, member):
        if isinstance(member, StructMember) and (member.size and member.numeric_size is None):
            # unknown array size
            warn('%s::%s array has unknown size "%s"' % (node_.name, member.name, member.size))
            size_alignment = (None, None)
        elif member.definition:
            size_alignment = evaluate_node_size(node_=member.definition, parent=node_, member=member)
        elif member.type_ in BUILTIN_SIZES:
            byte_size = BUILTIN_SIZES[member.type_]
            size_alignment = (byte_size, byte_size)
        else:
            # unknown type
            warn('%s::%s has unknown type "%s"' % (node_.name, member.name, member.type_))
            size_alignment = (None, None)
        member.byte_size, member.alignment = size_alignment
        return size_alignment != (None, None)

    def evaluate_empty_size(node_):
        node_.byte_size, node_.alignment = (None, None)

    def evaluate_members_sizes(node_):
        if not all([evaluate_member_size(node_, mem_) for mem_ in node_.members]):
            evaluate_empty_size(node_)
            return False
        return True

    def evaluate_partial_padding_size(node_):
        parts = split_after(node_.members, lambda m: (m.kind == Kind.DYNAMIC) or (m.array and not m.size))
        for part in [x for x in parts][1:]:
            part[0].alignment = max(part[0].alignment, max(x.alignment for x in part))

    def evaluate_struct_size(node_):
        def is_member_dynamic(m):
            return m.dynamic or m.greedy or m.kind != Kind.FIXED

        alignment = node_.members and max(x.alignment for x in node_.members) or 1
        byte_size = 0
        prev_member = node_.members and node_.members[0] or None
        for member in node_.members:
            padding = (member.alignment - byte_size % member.alignment) % member.alignment
            byte_size += member.byte_size + padding
            if is_member_dynamic(prev_member) and (prev_member.alignment < member.alignment):
                prev_member.padding = -member.alignment
            else:
                prev_member.padding = padding
            prev_member = member
        if node_.members:
            padding = (alignment - byte_size % alignment) % alignment
            byte_size += padding
            if any(is_member_dynamic(m) for m in node_.members):
                prev_member.padding = (node_.members[-1].alignment < alignment) and (-alignment) or 0
            else:
                prev_member.padding = padding
        node_.byte_size, node_.alignment = byte_size, alignment

    def evaluate_union_size(node_):
        node_.alignment = max(DISC_SIZE, node_.members and max(x.alignment for x in node_.members) or 1)
        node_.byte_size = (node_.members and max(x.byte_size for x in node_.members) or 0) + node_.alignment
        node_.byte_size = int((node_.byte_size + node_.alignment - 1) / node_.alignment) * node_.alignment

    for node in nodes:
        if isinstance(node, Struct):
            if evaluate_members_sizes(node):
                [evaluate_array_and_optional_size(mem) for mem in node.members]
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


class ModelParser():
    def __init__(self, parser, patcher, emit):
        self.parser = parser
        self.patcher = patcher
        self.emit = emit

    def __call__(self, *parse_args):
        nodes = self.parser.parse(*parse_args)
        if self.patcher:
            self.patcher(nodes)
        topological_sort(nodes)
        cross_reference(nodes, warn=self.emit.warn)
        evaluate_stiffness_kinds(nodes)
        evaluate_sizes(nodes, warn=self.emit.warn)
        return nodes
