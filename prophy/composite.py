from .six import ifilter, long, b

from . import scalar
from .exception import ProphyError
from .base_array import base_array
from _functools import partial
from .kind import kind

def validate(descriptor):
    if any(type_._UNLIMITED for _, type_ in descriptor[:-1]):
        raise ProphyError("unlimited field is not the last one")

def add_attributes(cls, descriptor):
    cls._SIZE = sum((type_._OPTIONAL and type_._OPTIONAL_SIZE or type_._SIZE) for _, type_ in descriptor)
    cls._DYNAMIC = any(type_._DYNAMIC for _, type_ in descriptor)
    cls._UNLIMITED = any(type_._UNLIMITED for _, type_ in descriptor)
    cls._OPTIONAL = False
    cls._BOUND = None
    cls._ALIGNMENT = max((type_._OPTIONAL and type_._OPTIONAL_ALIGNMENT or type_._ALIGNMENT) for _, type_ in descriptor) if descriptor else 1
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
    index, (name, tp) = next(ifilter(lambda enumed_field: enumed_field[1][0] is container_tp._BOUND, enumerate(descriptor)))
    bound_shift = container_tp._BOUND_SHIFT

    if tp._OPTIONAL:
        raise ProphyError("array must not be bound to optional field")
    if not issubclass(tp, (int, long)):
        raise ProphyError("array must be bound to an unsigned integer")

    if tp.__name__ == "container_len":
        def is_bound_shift_valid():
            _, t = next(ifilter(lambda field: field[0] in tp._BOUND, descriptor))
            return t._BOUND_SHIFT == bound_shift

        tp.add_bounded_container(container_name)
        if not is_bound_shift_valid():
            raise ProphyError("Different bound shifts are unsupported in externally sized arrays")
    else:
        class container_len(tp):
            _BOUND = [container_name]

            @staticmethod
            def add_bounded_container(cont_name):
                container_len._BOUND.append(cont_name)

            @staticmethod
            def evaluate(parent):
                result = len(getattr(parent, container_len._BOUND[0]))

                for array_name in container_len._BOUND[1:]:
                    if result != len(getattr(parent, array_name)):
                        raise ProphyError("Size mismatch of arrays in {}: {}"
                                          .format(parent.__class__.__name__,
                                                  ", ".join(container_len._BOUND)))
                return result

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
    for i, (name, type_) in enumerate(descriptor):
        descriptor[i] = (name, type_, get_encode_function(type_), get_decode_function(type_))

def get_encode_function(type_):
    if type_._OPTIONAL:
        type_._encode = staticmethod(get_encode_function(type_.__bases__[0]))
        return encode_optional
    elif type_._BOUND and issubclass(type_, (int, long)):
        return encode_array_delimiter
    elif issubclass(type_, base_array):
        return encode_array
    elif issubclass(type_, (struct, union)):
        return encode_composite
    elif issubclass(type_, bytes):
        return encode_bytes
    else:
        return encode_scalar

def encode_optional(parent, type_, value, endianness):
    if value is None:
        return b"\x00" * type_._OPTIONAL_SIZE
    else:
        return (type_._optional_type._encode(True, endianness).ljust(type_._OPTIONAL_ALIGNMENT, b'\x00')
                + type_._encode(parent, type_.__bases__[0], value, endianness))

def encode_array_delimiter(parent, type_, value, endianness):
    return type_._encode(type_.evaluate(parent), endianness)

def encode_array(parent, type_, value, endianness):
    return value._encode_impl(endianness)

def encode_composite(parent, type_, value, endianness):
    return value.encode(endianness, terminal = False)

def encode_bytes(parent, type_, value, endianness):
    return type_._encode(value)

def encode_scalar(parent, type_, value, endianness):
    return type_._encode(value, endianness)

def get_decode_function(type_):
    if type_._OPTIONAL:
        type_._decode = staticmethod(get_decode_function(type_.__bases__[0]))
        return decode_optional
    elif type_._BOUND and issubclass(type_, (int, long)):
        return decode_array_delimiter
    elif issubclass(type_, base_array):
        return decode_array
    elif issubclass(type_, (struct, union)):
        return decode_composite
    elif issubclass(type_, bytes):
        return decode_bytes
    else:
        return decode_scalar

def decode_optional(parent, name, type_, data, pos, endianness, len_hints):
    value, _ = type_._optional_type._decode(data, pos, endianness)
    if value:
        setattr(parent, name, True)
        return type_._OPTIONAL_ALIGNMENT + type_._decode(parent, name, type_.__bases__[0], data, pos + type_._OPTIONAL_ALIGNMENT, endianness, len_hints)
    else:
        setattr(parent, name, None)
        return type_._OPTIONAL_ALIGNMENT + type_._SIZE

def decode_array_delimiter(parent, name, type_, data, pos, endianness, len_hints):
    value, size = type_._decode(data, pos, endianness)
    if value < 0:
        raise ProphyError("Array delimiter must have positive value")
    for array_name in type_._BOUND:
        len_hints[array_name] = value
    return size

def decode_array(parent, name, type_, data, pos, endianness, len_hints):
    return getattr(parent, name)._decode_impl(data, pos, endianness, len_hints.get(name))

def decode_composite(parent, name, type_, data, pos, endianness, len_hints):
    return getattr(parent, name)._decode_impl(data, pos, endianness, terminal = False)

def decode_bytes(parent, name, type_, data, pos, endianness, len_hints):
    value, size = type_._decode(data, pos, len_hints.get(name))
    setattr(parent, name, value)
    return size

def decode_scalar(parent, name, type_, data, pos, endianness, len_hints):
    value, size = type_._decode(data, pos, endianness)
    setattr(parent, name, value)
    return size

def indent(text, spaces):
    return '\n'.join(x and spaces * ' ' + x or '' for x in text.split('\n'))

def field_to_string(name, type_, value):
    if issubclass(type_, base_array):
        return "".join(field_to_string(name, type_._TYPE, elem) for elem in value)
    elif issubclass(type_, (struct, union)):
        return "%s {\n%s}\n" % (name, indent(str(value), spaces = 2))
    elif issubclass(type_, bytes):
        return "%s: %s\n" % (name, repr(b(value)))
    elif issubclass(type_, scalar.enum):
        return "%s: %s\n" % (name, type_._int_to_name[value])
    else:
        return "%s: %s\n" % (name, value)

def get_kind(type_):
    if issubclass(type_, base_array):
        return kind.ARRAY
    elif issubclass(type_, struct):
        return kind.STRUCT
    elif issubclass(type_, union):
        return kind.UNION
    elif issubclass(type_, bytes):
        return kind.BYTES
    elif issubclass(type_, scalar.enum):
        return kind.ENUM
    else:
        return kind.INT


def field_to_list(prefix, name, type_, value):

    if issubclass(type_, base_array):
        array = []
        for idx,elem in enumerate(value):
            arr_idx = '{}.{}[{}]'.format(prefix,name,idx)
            array += field_to_list(arr_idx, '', type_._TYPE, elem)
        return array

    elif issubclass(type_, (struct, union)):
        prefix = fix_prefix(prefix,name)
        return value.fields(prefix)
    else:
        field = fix_prefix(prefix,name)[1:]
        return [field]

def field_to_dict(prefix, name, type_, value):

    if issubclass(type_, base_array):
        array = {}
        for idx,elem in enumerate(value):
            arr_idx = '{}.{}[{}]'.format(prefix,name,idx)
            array.update(field_to_dict(arr_idx, '', type_._TYPE, elem))
        return array

    elif issubclass(type_, (struct, union)):
        prefix = fix_prefix(prefix,name)
        return value.values(prefix)
    else:
        field = fix_prefix(prefix,name)[1:]
        return dict([(field,value)])

def fix_prefix(prefix,name):
    if name:
        return "{}.{}".format(prefix,name)
    else:
        return "{}".format(prefix)

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

    @classmethod
    def get_descriptor(cls):
        descriptor = []
        for name, tp, _, _ in cls._descriptor:
            elem = FieldDescriptor(name, tp, get_kind(tp))
            descriptor.append(elem)
        return descriptor

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
    if any(type_._DYNAMIC for _, type_, _ in descriptor):
        raise ProphyError("dynamic types not allowed in union")
    if any(type_._BOUND for _, type_, _ in descriptor):
        raise ProphyError("bound array/bytes not allowed in union")
    if any(issubclass(type_, base_array) for _, type_, _ in descriptor):
        raise ProphyError("static array not implemented in union")
    if any(type_._OPTIONAL for _, type_, _ in descriptor):
        raise ProphyError("union with optional field disallowed")

def add_union_attributes(cls, descriptor):
    def pad(value, alignment):
        remainder = value % alignment
        return remainder and (value + (alignment - remainder)) or value
    cls._discriminator_type = scalar.u32
    cls._DYNAMIC = False
    cls._UNLIMITED = False
    cls._OPTIONAL = False
    cls._ALIGNMENT = max(scalar.u32._ALIGNMENT, max(type_._ALIGNMENT for _, type_, _ in descriptor))
    cls._SIZE = pad(cls._ALIGNMENT + max(type_._SIZE for _, type_, _ in descriptor), cls._ALIGNMENT)
    cls._BOUND = None
    cls._PARTIAL_ALIGNMENT = None

def add_union_properties(cls, descriptor):
    add_union_discriminator(cls)
    for field in descriptor:
        name, type_, disc, _, _ = field
        if issubclass(type_, (struct, union)):
            add_union_composite(cls, name, type_, disc, field)
        else:
            add_union_scalar(cls, name, type_, disc, field)

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

def add_union_scalar(cls, name, type_, disc, field):
    def getter(self):
        if self._discriminated is not field:
            raise ProphyError("currently field %s is discriminated" % self._discriminated[2])
        return self._fields.get(name, type_._DEFAULT)
    def setter(self, new_value):
        if self._discriminated is not field:
            raise ProphyError("currently field %s is discriminated" % self._discriminated[2])
        new_value = type_._check(new_value)
        self._fields[name] = new_value
    setattr(cls, name, property(getter, setter))

def add_union_composite(cls, name, type_, disc, field):
    def getter(self):
        if self._discriminated is not field:
            raise ProphyError("currently field %s is discriminated" % self._discriminated[2])
        value = self._fields.get(name)
        if value is None:
            value = type_()
            value = self._fields.setdefault(name, value)
        return value
    def setter(self, new_value):
        raise ProphyError("assignment to composite field not allowed")
    setattr(cls, name, property(getter, setter))

def extend_union_descriptor(cls, descriptor):
    for i, (name, type_, disc) in enumerate(descriptor):
        descriptor[i] = (name, type_, disc, get_encode_function(type_), get_decode_function(type_))

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

    def get_discriminated(self):
        name, tp, _, _, _  =  self._discriminated
        return FieldDescriptor(name, tp, get_kind(tp))

    @classmethod
    def get_descriptor(cls):
        descriptor = []
        for name, tp, _, _, _ in cls._descriptor:
            elem = FieldDescriptor(name, tp, get_kind(tp))
            descriptor.append(elem)
        return descriptor

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
        name, type_, _, _, decode_ = field
        self._discriminated = field
        decode_(self, name, type_, data, pos + self._ALIGNMENT, endianness, {})
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
        name, type_, _, _, _ = self._discriminated
        rhs = getattr(other, name)
        if issubclass(type_, (struct, union)):
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

class FieldDescriptor(object):
    def __init__(self, name, type_, kind):
        self.name = name
        self.type = type_
        self.kind = kind
    def __repr__(self):
        return ("<{}, {}, {}>".format(self.name, self.kind, self.type))
