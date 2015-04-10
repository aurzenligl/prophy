from .six import ifilter, long, b

from . import scalar
from .exception import ProphyError
from .base_array import base_array

def validate(descriptor):
    if any(type._UNLIMITED for _, type in descriptor[:-1]):
        raise ProphyError("unlimited field is not the last one")

def add_attributes(cls, descriptor):
    cls._SIZE = sum((type._OPTIONAL and type._OPTIONAL_SIZE or type._SIZE) for _, type in descriptor)
    cls._DYNAMIC = any(type._DYNAMIC for _, type in descriptor)
    cls._UNLIMITED = any(type._UNLIMITED for _, type in descriptor)
    cls._OPTIONAL = False
    cls._BOUND = None
    cls._ALIGNMENT = max((type._OPTIONAL and type._OPTIONAL_ALIGNMENT or type._ALIGNMENT) for _, type in descriptor) if descriptor else 1
    cls._PARTIAL_ALIGNMENT = None

    alignment = 1
    for _, tp in reversed(descriptor):
        if issubclass(tp, (base_array, bytes)) and tp._DYNAMIC:
            tp._PARTIAL_ALIGNMENT = alignment
            alignment = 1
        alignment = max(tp._ALIGNMENT, alignment)

class Padder(object):
    def __init__(self):
        self.offset = 0
    def __call__(self, size, alignment):
        self.offset += size
        padding = (alignment - self.offset % alignment) % alignment
        self.offset += padding
        return padding

def add_padding(cls, descriptor):
    if not descriptor:
        return

    sizes = [tp._SIZE for _, tp in descriptor]
    alignments = [tp._ALIGNMENT for _, tp in descriptor[1:]] + [cls._ALIGNMENT]
    paddings = map(Padder(), sizes, alignments)
    cls._SIZE += sum(paddings)

def add_properties(cls, descriptor):
    for name, tp in descriptor:
        if issubclass(tp, base_array):
            add_repeated(cls, name, tp)
        elif issubclass(tp, (struct, union)):
            add_composite(cls, name, tp)
        else:
            add_scalar(cls, name, tp)

def add_repeated(cls, name, tp):
    def getter(self):
        value = self._fields.get(name)
        if value is None:
            value = tp()
            self._fields[name] = value
        return value
    def setter(self, new_value):
        raise ProphyError("assignment to array field not allowed")
    setattr(cls, name, property(getter, setter))
    if tp._BOUND:
        substitute_len_field(cls, cls._descriptor, name, tp)

def add_scalar(cls, field_name, field_type):
    if field_type._OPTIONAL:
        def getter(self):
            return self._fields.get(field_name)
        def setter(self, new_value):
            self._fields[field_name] = None if new_value is None else field_type._check(new_value)
    else:
        def getter(self):
            return self._fields.get(field_name, field_type._DEFAULT)
        def setter(self, new_value):
            self._fields[field_name] = field_type._check(new_value)
    setattr(cls, field_name, property(getter, setter))
    if field_type._BOUND:
        substitute_len_field(cls, cls._descriptor, field_name, field_type)

def add_composite(cls, name, tp):
    if tp._OPTIONAL:
        def getter(self):
            return self._fields.get(name)
        def setter(self, new_value):
            if new_value is True:
                self._fields[name] = tp()
            elif new_value is None:
                self._fields.pop(name, None)
            else:
                raise ProphyError("assignment to composite field not allowed")
    else:
        def getter(self):
            value = self._fields.get(name)
            if value:
                return value
            else:
                return self._fields.setdefault(name, tp())
        def setter(self, new_value):
            raise ProphyError("assignment to composite field not allowed")
    setattr(cls, name, property(getter, setter))

def substitute_len_field(cls, descriptor, container_name, container_tp):
    index, field = next(ifilter(lambda x: x[1][0] is container_tp._BOUND, enumerate(descriptor)))
    name, tp = field
    bound_shift = container_tp._BOUND_SHIFT

    if tp._OPTIONAL:
        raise ProphyError("array must not be bound to optional field")
    if not issubclass(tp, (int, long)):
        raise ProphyError("array must be bound to an unsigned integer")

    class container_len(tp):
        _BOUND = container_name

        @staticmethod
        def _encode(value, endianness):
            return tp._encode(value + bound_shift, endianness)

        @staticmethod
        def _decode(data, pos, endianness):
            value, size = tp._decode(data, pos, endianness)
            array_guard = 65536
            if value > array_guard:
                raise ProphyError("decoded array length over %s" % array_guard)
            value -= bound_shift
            if value < 0:
                raise ProphyError("decoded array length smaller than shift")
            return value, size

    descriptor[index] = (name, container_len)
    delattr(cls, name)

def extend_descriptor(cls, descriptor):
    for i, (name, type) in enumerate(descriptor):
        descriptor[i] = (name, type, get_encode_function(type), get_decode_function(type))

def get_encode_function(type):
    if type._OPTIONAL:
        type._encode = staticmethod(get_encode_function(type.__bases__[0]))
        return encode_optional
    elif type._BOUND and issubclass(type, (int, long)):
        return encode_array_delimiter
    elif issubclass(type, base_array):
        return encode_array
    elif issubclass(type, (struct, union)):
        return encode_composite
    elif issubclass(type, bytes):
        return encode_bytes
    else:
        return encode_scalar

def encode_optional(parent, type, value, endianness):
    if value is None:
        return b"\x00" * type._OPTIONAL_SIZE
    else:
        return (type._optional_type._encode(True, endianness).ljust(type._OPTIONAL_ALIGNMENT, b'\x00')
                + type._encode(parent, type.__bases__[0], value, endianness))

def encode_array_delimiter(parent, type, value, endianness):
    return type._encode(len(getattr(parent, type._BOUND)), endianness)

def encode_array(parent, type, value, endianness):
    return value._encode_impl(endianness)

def encode_composite(parent, type, value, endianness):
    return value.encode(endianness, terminal = False)

def encode_bytes(parent, type, value, endianness):
    return type._encode(value)

def encode_scalar(parent, type, value, endianness):
    return type._encode(value, endianness)

def get_decode_function(type):
    if type._OPTIONAL:
        type._decode = staticmethod(get_decode_function(type.__bases__[0]))
        return decode_optional
    elif type._BOUND and issubclass(type, (int, long)):
        return decode_array_delimiter
    elif issubclass(type, base_array):
        return decode_array
    elif issubclass(type, (struct, union)):
        return decode_composite
    elif issubclass(type, bytes):
        return decode_bytes
    else:
        return decode_scalar

def decode_optional(parent, name, type, data, pos, endianness, len_hints):
    value, _ = type._optional_type._decode(data, pos, endianness)
    if value:
        setattr(parent, name, True)
        return type._OPTIONAL_ALIGNMENT + type._decode(parent, name, type.__bases__[0], data, pos + type._OPTIONAL_ALIGNMENT, endianness, len_hints)
    else:
        setattr(parent, name, None)
        return type._OPTIONAL_ALIGNMENT + type._SIZE

def decode_array_delimiter(parent, name, type, data, pos, endianness, len_hints):
    value, size = type._decode(data, pos, endianness)
    len_hints[type._BOUND] = value
    return size

def decode_array(parent, name, type, data, pos, endianness, len_hints):
    return getattr(parent, name)._decode_impl(data, pos, endianness, len_hints.get(name))

def decode_composite(parent, name, type, data, pos, endianness, len_hints):
    return getattr(parent, name)._decode_impl(data, pos, endianness, terminal = False)

def decode_bytes(parent, name, type, data, pos, endianness, len_hints):
    value, size = type._decode(data, pos, len_hints.get(name))
    setattr(parent, name, value)
    return size

def decode_scalar(parent, name, type, data, pos, endianness, len_hints):
    value, size = type._decode(data, pos, endianness)
    setattr(parent, name, value)
    return size

def indent(text, spaces):
    return '\n'.join(x and spaces * ' ' + x or '' for x in text.split('\n'))

def field_to_string(name, type, value):
    if issubclass(type, base_array):
        return "".join(field_to_string(name, type._TYPE, elem) for elem in value)
    elif issubclass(type, (struct, union)):
        return "%s {\n%s}\n" % (name, indent(str(value), spaces = 2))
    elif issubclass(type, bytes):
        return "%s: %s\n" % (name, repr(b(value)))
    elif issubclass(type, scalar.enum):
        return "%s: %s\n" % (name, type._int_to_name[value])
    else:
        return "%s: %s\n" % (name, value)

def validate_copy_from(lhs, rhs):
    if not isinstance(rhs, lhs.__class__):
        raise TypeError("Parameter to copy_from must be instance of same class.")

def set_field(parent, name, rhs):
    lhs = getattr(parent, name)
    if isinstance(rhs, base_array):
        if issubclass(rhs._TYPE, (struct, union)):
            if rhs._DYNAMIC:
                del lhs[:]
                lhs.extend(rhs[:])
            else:
                for lhs_elem, rhs_elem in zip(lhs, rhs):
                    lhs_elem.copy_from(rhs_elem)
        else:
            lhs[:] = rhs[:]
    elif isinstance(rhs, (struct, union)):
        lhs.copy_from(rhs)
    else:
        parent._fields[name] = rhs

class struct(object):
    __slots__ = []

    def __init__(self):
        self._fields = {}

    def __str__(self):
        out = ""
        for name, tp, _, _ in self._descriptor:
            value = getattr(self, name, None)
            if value is not None:
                out += field_to_string(name, tp, value)
        return out

    @staticmethod
    def _get_padding(offset, alignment):
        remainder = offset % alignment
        if remainder:
            return b'\x00' * (alignment - remainder)
        else:
            return b''

    @staticmethod
    def _get_padding_size(offset, alignment):
        remainder = offset % alignment
        return alignment - remainder if remainder else 0

    def encode(self, endianness, terminal = True):
        data = b""

        for name, tp, encode_, _ in self._descriptor:
            data += (self._get_padding(len(data), tp._ALIGNMENT) +
                     encode_(self, tp, getattr(self, name, None), endianness))
            if tp._PARTIAL_ALIGNMENT:
                data += self._get_padding(len(data), tp._PARTIAL_ALIGNMENT)

        data += self._get_padding(len(data), self._ALIGNMENT)

        return data

    def decode(self, data, endianness):
        return self._decode_impl(data, 0, endianness, terminal = True)

    def _decode_impl(self, data, pos, endianness, terminal):
        len_hints = {}
        start_pos = pos

        for name, tp, _, decode_ in self._descriptor:
            pos += self._get_padding_size(pos, tp._ALIGNMENT)
            pos += decode_(self, name, tp, data, pos, endianness, len_hints)
            if tp._PARTIAL_ALIGNMENT:
                pos += self._get_padding_size(pos, tp._PARTIAL_ALIGNMENT)

        pos += self._get_padding_size(pos, self._ALIGNMENT)

        if terminal and pos < len(data):
            raise ProphyError("not all bytes read")

        return pos - start_pos

    def copy_from(self, other):
        validate_copy_from(self, other)
        if other is self:
            return

        self._fields.clear()
        for name, rhs in other._fields.items():
            set_field(self, name, rhs)

class struct_packed(struct):
    __slots__ = []
    @staticmethod
    def _get_padding(offset, alignment):
        return b''
    @staticmethod
    def _get_padding_size(offset, alignment):
        return 0

class struct_generator(type):
    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = ["_fields"]
        return super(struct_generator, cls).__new__(cls, name, bases, attrs)
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "_generated"):
            cls._generated = True
            descriptor = cls._descriptor
            validate(descriptor)
            add_attributes(cls, descriptor)
            if not issubclass(cls, struct_packed):
                add_padding(cls, descriptor)
            add_properties(cls, descriptor)
            extend_descriptor(cls, descriptor)
        super(struct_generator, cls).__init__(name, bases, attrs)

def validate_union(descriptor):
    if any(type._DYNAMIC for _, type, _ in descriptor):
        raise ProphyError("dynamic types not allowed in union")
    if any(type._BOUND for _, type, _ in descriptor):
        raise ProphyError("bound array/bytes not allowed in union")
    if any(issubclass(type, base_array) for _, type, _ in descriptor):
        raise ProphyError("static array not implemented in union")
    if any(type._OPTIONAL for _, type, _ in descriptor):
        raise ProphyError("union with optional field disallowed")

def add_union_attributes(cls, descriptor):
    def pad(value, alignment):
        remainder = value % alignment
        return remainder and (value + (alignment - remainder)) or value
    cls._discriminator_type = scalar.u32
    cls._DYNAMIC = False
    cls._UNLIMITED = False
    cls._OPTIONAL = False
    cls._ALIGNMENT = max(scalar.u32._ALIGNMENT, max(type._ALIGNMENT for _, type, _ in descriptor))
    cls._SIZE = pad(cls._ALIGNMENT + max(type._SIZE for _, type, _ in descriptor), cls._ALIGNMENT)
    cls._BOUND = None
    cls._PARTIAL_ALIGNMENT = None

def add_union_properties(cls, descriptor):
    add_union_discriminator(cls)
    for field in descriptor:
        name, type, disc, _, _ = field
        if issubclass(type, (struct, union)):
            add_union_composite(cls, name, type, disc, field)
        else:
            add_union_scalar(cls, name, type, disc, field)

def add_union_discriminator(cls):
    def getter(self):
        return self._discriminated[2]
    def setter(self, new_value):
        field = next(ifilter(lambda x: new_value in (x[0], x[2]), self._descriptor), None)
        if field:
            if field != self._discriminated:
                self._discriminated = field
                self._fields = {}
        else:
            raise ProphyError("unknown discriminator")
    setattr(cls, "discriminator", property(getter, setter))

def add_union_scalar(cls, name, type, disc, field):
    def getter(self):
        if self._discriminated is not field:
            raise ProphyError("currently field %s is discriminated" % self._discriminated[2])
        return self._fields.get(name, type._DEFAULT)
    def setter(self, new_value):
        if self._discriminated is not field:
            raise ProphyError("currently field %s is discriminated" % self._discriminated[2])
        new_value = type._check(new_value)
        self._fields[name] = new_value
    setattr(cls, name, property(getter, setter))

def add_union_composite(cls, name, type, disc, field):
    def getter(self):
        if self._discriminated is not field:
            raise ProphyError("currently field %s is discriminated" % self._discriminated[2])
        value = self._fields.get(name)
        if value is None:
            value = type()
            value = self._fields.setdefault(name, value)
        return value
    def setter(self, new_value):
        raise ProphyError("assignment to composite field not allowed")
    setattr(cls, name, property(getter, setter))

def extend_union_descriptor(cls, descriptor):
    for i, (name, type, disc) in enumerate(descriptor):
        descriptor[i] = (name, type, disc, get_encode_function(type), get_decode_function(type))

def get_discriminated_field(cls, discriminator):
    field = next((x for x in cls._descriptor if x[2] == discriminator), None)
    return field

class union(object):
    __slots__ = []

    def __init__(self):
        self._fields = {}
        self._discriminated = self._descriptor[0]

    def __str__(self):
        name, tp, _, _, _ = self._discriminated
        value = getattr(self, name)
        return field_to_string(name, tp, value)

    def encode(self, endianness, terminal = True):
        name, tp, disc, encode_, _ = self._discriminated
        value = getattr(self, name)
        data = (self._discriminator_type._encode(disc, endianness).ljust(self._ALIGNMENT, b'\x00')
                + encode_(self, tp, value, endianness))
        return data.ljust(self._SIZE, b'\x00')

    def decode(self, data, endianness):
        return self._decode_impl(data, 0, endianness, terminal = True)

    def _decode_impl(self, data, pos, endianness, terminal):
        disc, _ = self._discriminator_type._decode(data, pos, endianness)
        field = get_discriminated_field(self, disc)
        if not field:
            raise ProphyError("unknown discriminator")
        name, type, _, _, decode_ = field
        self._discriminated = field
        decode_(self, name, type, data, pos + self._ALIGNMENT, endianness, {})
        if (len(data) - pos) < self._SIZE:
            raise ProphyError("not enough bytes")
        if terminal and (len(data) - pos) > self._SIZE:
            raise ProphyError("not all bytes read")
        return self._SIZE

    def copy_from(self, other):
        validate_copy_from(self, other)
        if other is self:
            return

        self._fields.clear()
        self._discriminated = other._discriminated
        name, type, _, _, _ = self._discriminated
        rhs = getattr(other, name)
        if issubclass(type, (struct, union)):
            lhs = getattr(self, name)
            lhs.copy_from(rhs)
        else:
            setattr(self, name, rhs)

class union_generator(type):
    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = ["_fields", "_discriminated"]
        return super(union_generator, cls).__new__(cls, name, bases, attrs)
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "_generated"):
            cls._generated = True
            descriptor = cls._descriptor
            validate_union(descriptor)
            add_union_attributes(cls, descriptor)
            extend_union_descriptor(cls, descriptor)
            add_union_properties(cls, descriptor)
        super(union_generator, cls).__init__(name, bases, attrs)
