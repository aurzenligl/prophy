from itertools import islice

import renew

from . import calc, six

""" Exception types """


class ParseError(Exception):
    def __init__(self, errors):
        Exception.__init__(self, "parsing error")
        self.errors = errors
        """Collection of 2-tuples of location and message."""


class ModelError(Exception):
    """ General error for model tree construction errors. """
    pass


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


class ModelNode(renew.Mold):
    _cls_namespace = "prophyc.model"
    """ The lowermost base for each type of prophyc model. """
    __slots__ = "name", "_value", "docstring"
    _eq_attributes = "name", "_value"
    _str_pattern = None

    def __init__(self, name, value, docstring=None):
        self.name = _check_string(name, "model node name")
        self._value = value
        self.docstring = _check_string(docstring, "doc string")

    @property
    def value(self):
        return self._value

    def __str__(self):
        return self.schema_repr()

    def schema_repr(self):
        return self._str_pattern.format(s=self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return all(getattr(self, a) == getattr(other, a) for a in self._eq_attributes)

        if isinstance(other, tuple) and len(other) in (2, 3):
            return all(getattr(self, a) == other[i] for i, a in enumerate(self._eq_attributes))

    def __ne__(self, other):
        return not self.__eq__(other)

    def dependencies(self):
        raise NotImplementedError("To be overridden in %s class." % self.__class__.__name__)


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

    def dependencies(self):
        def sub_(x, y):
            return x.replace(y, " ")

        for symbol in six.reduce(sub_, "()+-", self.value).split():
            if not symbol.isdigit():
                yield symbol


class EnumMember(Constant):
    _str_pattern = "{s.name} = {s.value!r};"
    __slots__ = ()


class _Serializable(ModelNode):
    _cls_make_slots = False
    __slots__ = "kind", "byte_size", "alignment"

    def __init__(self, name, value, docstring=None):
        super(_Serializable, self).__init__(name, value, docstring)
        self.alignment = None
        """byte size of field influenced by array: multiplied by fixed/limited size, 0 if dynamic/greedy"""
        self.byte_size = None
        """type kind, not influenced by array or optional"""
        self.kind = None
        self.calc_wire_stiffness()

    @classmethod
    def calc_wire_stiffness(cls):
        raise NotImplementedError("Abstract method to be overriden in %s" % cls.__name__)


class Typedef(_Serializable):
    _str_pattern = "typedef {s.type_name} {s.name};"
    _eq_attributes = "name", "type_name", "definition"
    __slots__ = "definition",

    def __init__(self, name, type_name, definition=None, docstring=None):
        if definition is not None:
            if not isinstance(definition, six.string_types + (Typedef, Enum, Struct, Union)):
                msg = "{}.definition should be string, Typedef, Enum, Struct or Union, got: {}."
                raise ModelError(msg.format(self.__class__.__name__, type(definition).__name__))
        self.definition = definition
        super(Typedef, self).__init__(name, type_name, docstring)

    @property
    def type_name(self):
        return self._value

    @type_name.setter
    def type_name(self, new_value):
        _check_string(new_value, "Type designator")
        self._value = new_value

    @property
    def lowermost_typedef(self):
        lowermost = self.definition
        while isinstance(lowermost, Typedef):
            lowermost = lowermost.definition
        return lowermost

    def calc_wire_stiffness(self):
        """ Typedef propagates stiffness kinds of its lowermost type """
        self.kind = Kind.FIXED
        if self.definition and isinstance(self.lowermost_typedef, Struct):
            self.kind = self.lowermost_typedef.kind

    def dependencies(self):
        yield self.type_name


class StructMember(Typedef):
    __slots__ = "bound", "size", "greedy", "optional", "numeric_size", "padding"
    _eq_attributes = "name", "_value", "bound", "size", "greedy", "optional", "definition"

    def __init__(self, name, type_name, definition=None, bound=None, size=None, greedy=False, optional=False,
                 docstring=None):
        assert sum((bool(bound or size), greedy, optional)) <= 1, "Over-constraint"
        assert isinstance(optional, bool), "'optional' argument value has to be boolean"
        assert isinstance(greedy, bool), "'greedy' argument value has to be boolean"

        super(StructMember, self).__init__(name, type_name, definition, docstring)
        self.bound = bound
        self.size = size
        self.greedy = greedy
        self.optional = optional

        """integral number indicating array size (it may be a string with enum member or constant name)"""
        self.numeric_size = None
        """amount of bytes to add before next field. If field dynamic: negative alignment of next field"""
        self.padding = None

    @property
    def is_array(self):
        return self.bound or self.size or self.greedy

    @property
    def is_fixed(self):
        return not self.bound and self.size

    @property
    def is_limited(self):
        return self.bound and self.size

    @property
    def is_dynamic(self):
        return self.bound and not self.size

    def __str__(self):
        return self.schema_repr()

    def schema_repr(self):
        if self.optional:
            return '{s.type_name}* {s.name};'.format(s=self)
        if self.is_fixed:
            return '{s.type_name} {s.name}[{s.size}];'.format(s=self)
        if self.is_limited:
            return '{s.type_name} {s.name}<{s.size}>;'.format(s=self)
        if self.is_dynamic:
            return '{s.type_name} {s.name}<@{s.bound}>;'.format(s=self)
        if self.greedy:
            return '{s.type_name} {s.name}<...>;'.format(s=self)

        return '{s.type_name} {s.name};'.format(s=self)


class UnionMember(Typedef):
    _str_pattern = '{s.discriminator}: {s.type_name} {s.name};'
    _eq_attributes = "name", "type_name", "discriminator"
    __slots__ = "discriminator",

    def __init__(self, name, type_name, discriminator, definition=None, docstring=None):
        super(UnionMember, self).__init__(name, type_name, definition, docstring)
        self.discriminator = discriminator


""" Composite kinds """


class _Container(ModelNode):
    """ Anything that represents a collection of members. """
    _cls_make_slots = False
    _member_type_restriction = None
    _collection_kind = None
    _str_pattern = "{s._collection_kind} {s.name} {{\n{s._str_members}}};\n"
    __slots__ = ()

    def __init__(self, name, members, docstring=None):
        super(_Container, self).__init__(name, members, docstring)
        self._check_members_type(members)
        self._check_members_duplication(members)

    def _check_members_type(self, members):
        if not isinstance(members, list):
            msg = "{s._collection_kind} '{s.name}' members must be a list, got {t} instead."
            raise ModelError(msg.format(s=self, t=type(members).__name__))

        for index, member in enumerate(members):
            if not isinstance(member, self._member_type_restriction):
                msg = "Each member of {s._collection_kind} '{s.name}' has to be a {et} instance. Got {gt} at index {i}."
                raise ModelError(
                    msg.format(s=self, et=self._member_type_restriction.__name__, gt=type(member).__name__, i=index))

    def _check_members_duplication(self, members):
        meet_identifiers = set()
        for member in members:
            if member.name in meet_identifiers:
                msg = "Duplicated '{m.name}' identifier in {s._collection_kind} {s.name}."
                raise ModelError(msg.format(m=member, s=self))
            meet_identifiers.add(member.name)

    @property
    def value(self):
        forbidden = "Use of value property is forbidden for {0}. Use '{0}.members' instead."
        raise ModelError(forbidden.format(self.__class__.__name__))

    @property
    def members(self):
        return self._value

    @property
    def _str_members(self):
        return "".join("    {}\n".format(m) for m in self.members)

    def dependencies(self):
        for member in self.members:
            for dependency in member.dependencies():
                yield dependency


class Include(_Container):
    _member_type_restriction = ModelNode
    _collection_kind = "include"
    _str_pattern = "#include {s.name};\n"
    __slots__ = ()

    def _check_members_duplication(self, members):
        """ Include is allowed to get duplicated definitions. """

    def dependencies(self):
        """ No need to provide any dependencies to include. """
        return []

    def defined_symbols(self):
        """ Generate collection of symbols delivered by this include. """
        for member in self.members:
            if isinstance(member, Include):
                for symbol in member.defined_symbols():
                    yield symbol
            else:
                yield member


class Enum(_Container):
    _member_type_restriction = EnumMember
    _collection_kind = "enum"
    __slots__ = ()

    def dependencies(self):
        for member in self.members:
            yield member.name


class _SerializableContainer(_Container, _Serializable):
    __slots__ = ()

    def calc_wire_stiffness(self):
        self._check_members_type(self.members)
        """ Evaluate stiffness of the node. """
        self.kind = Kind.FIXED
        if isinstance(self, Struct):
            if self.members:
                for member in self.members:
                    member.calc_wire_stiffness()

                if self.members[-1].greedy:
                    self.kind = Kind.UNLIMITED
                elif any(x.is_dynamic for x in self.members):
                    self.kind = Kind.DYNAMIC
                else:
                    self.kind = max(x.kind for x in self.members)


class Struct(_SerializableContainer):
    _member_type_restriction = StructMember
    _collection_kind = "struct"
    __slots__ = ()


class Union(_SerializableContainer):
    _member_type_restriction = UnionMember
    _collection_kind = "union"
    __slots__ = ()


""" Utils """


def _check_string(docstring, what_):
    if docstring is None:
        return
    if not isinstance(docstring, six.string_types):
        msg = "Got {} of '{}' type, expected string."
        raise ModelError(msg.format(what_, type(docstring).__name__))
    return six.decode_string(docstring)


def split_after(nodes, predicate):
    part = []
    for x in nodes:
        part.append(x)
        if predicate(x):
            yield part
            part = []
    if part:
        yield part


def null_warn(_):
    pass


""" Following functions process model. """


def topological_sort(nodes):
    """Sorts nodes."""

    def find_first_dep(dependency, start_index):
        for i, n in enumerate(islice(nodes, start_index, None), start_index):
            if n.name == dependency:
                return i

    def model_sort_rotate():
        node = nodes[index]
        for dep in node.dependencies():
            if dep not in known and dep in available:
                found_index = find_first_dep(dep, index + 1)
                if found_index:
                    nodes.insert(index, nodes.pop(found_index))
                return True
        known.add(node.name)

    known = set(x + y for x in "uir" for y in ["8", "16", "32", "64"])
    available = set(node.name for node in nodes)
    for index in range(len(nodes)):
        while model_sort_rotate():
            pass


def _make_types_index(nodes_):
    """ Creates flat dictionary that maps model objects to its name. """
    included = set()
    for node_ in nodes_:
        if isinstance(node_, Include):
            if node_.name not in included:
                included.add(node_.name)
                for included_name, included_type in _make_types_index(node_.members):
                    yield included_name, included_type
        else:
            yield node_.name, node_


def _collect_constants(nodes_, constants=None):
    constants = constants or {}
    included = set()
    for node_ in nodes_:
        if isinstance(node_, Include) and node_.name not in included:
            included.add(node_.name)
            constants.update(_collect_constants(node_.members, constants))

        elif isinstance(node_, Constant):
            constants[node_.name] = node_.eval_int(constants)

        elif isinstance(node_, Enum):
            for member in node_.members:
                constants[member.name] = member.eval_int(constants)

        elif isinstance(node_, Typedef):

            def get_last_in_chain(key):
                value = constants.get(key, key)
                return value if value == key else get_last_in_chain(value)

            constants[node_.name] = get_last_in_chain(node_.type_name)

    return constants


def cross_reference(nodes, warn=null_warn):
    """
    Adds definition reference to Typedef and StructMember.
    Adds numeric_size to StructMember if it's a sized array.
    """
    types_index = dict(_make_types_index(nodes))
    constants = _collect_constants(nodes)

    def cross_reference_types(node_):
        if node_.type_name in BUILTIN_SIZES:
            node_.definition = None
            return
        found = types_index.get(node_.type_name)
        if not found:
            warn("type '%s' not found" % node_.type_name)
        node_.definition = found

    def evaluate_array_sizes(node_):
        if node_.size:
            try:
                node_.numeric_size = to_int(node_.size, constants)
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

    return constants


def to_int(x, constants):
    try:
        return int(x)
    except ValueError:
        val = constants.get(x)
        return val if val is not None else calc.eval(x, constants)


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
        elif node_.type_name in BUILTIN_SIZES:
            byte_size = BUILTIN_SIZES[node_.type_name]
            return byte_size, byte_size
        else:
            # unknown type, e.g. empty typedef
            warn('%s::%s has unknown type "%s"' % (parent.name, member.name, node_.type_name))
            return None, None

    def evaluate_array_and_optional_size(member):
        if member.is_array and member.byte_size is not None:
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

        elif member.type_name in BUILTIN_SIZES:
            byte_size = BUILTIN_SIZES[member.type_name]
            size_alignment = (byte_size, byte_size)
        else:
            # unknown type
            warn('%s::%s has unknown type "%s"' % (node_.name, member.name, member.type_name))
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
        parts = split_after(node_.members, lambda m: (m.kind == Kind.DYNAMIC) or (m.is_array and not m.size))
        for part in [x for x in parts][1:]:
            part[0].alignment = max(part[0].alignment, max(x.alignment for x in part))

    def evaluate_struct_size(node_):
        def is_member_dynamic(m):
            return m.is_dynamic or m.greedy or m.kind != Kind.FIXED

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
        elif isinstance(node, Include):
            evaluate_sizes(node.members, warn)


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
        if member.kind == Kind.DYNAMIC or member.is_dynamic:
            current = []
            parts.append(current)
    if members:
        current.append(members[-1])
    return main, parts


def evaluate_model(nodes, warn_emitter=lambda x: None):
    topological_sort(nodes)
    constants = cross_reference(nodes, warn_emitter)
    evaluate_stiffness_kinds(nodes)
    evaluate_sizes(nodes, warn_emitter)
    return nodes, constants


class ModelParser(object):
    def __init__(self, parser, patcher, emit):
        self.parser = parser
        self.patcher = patcher
        self.emit = emit

    def __call__(self, *parse_args):
        nodes = self.parser.parse(*parse_args)
        if self.patcher:
            self.patcher(nodes)
        nodes, _ = evaluate_model(nodes, self.emit.warn)
        return nodes
