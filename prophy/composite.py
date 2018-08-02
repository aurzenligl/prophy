from collections import namedtuple

from . import scalar
from .base_array import base_array
from .exception import ProphyError
from .kind import kind
from .six import long, repr_bytes


def make_codec_gen(extended_type):
    def add_codecs(self):
        encode_fcn = get_encode_function(self.type)
        decode_fcn = get_decode_function(self.type)
        item_with_codecs = extended_type(*(self + (encode_fcn, decode_fcn)))
        return item_with_codecs
    return add_codecs


RawStructItem = namedtuple("RawStructItem", "name, type")
StructItem = namedtuple("StructItem", "name, type, encode_fcn, decode_fcn")
RawStructItem._add_codecs = make_codec_gen(StructItem)

RawUnionItem = namedtuple("RawUnionItem", "name, type, discriminator")
UnionItem = namedtuple("UnionItem", "name, type, discriminator, encode_fcn, decode_fcn")
RawUnionItem._add_codecs = make_codec_gen(UnionItem)


def distance_to_next_multiply(number, alignment):
    remainer = number % alignment
    return (alignment - remainer) % alignment


def build_container_length_field(sizer_item_type, container_name, bound_shift):
    class container_len(sizer_item_type):
        _BOUND = [container_name]

        @classmethod
        def add_bounded_container(cls, cont_name):
            cls._BOUND.append(cont_name)

        @classmethod
        def evaluate(cls, parent):
            sizes = set(len(getattr(parent, c_name)) for c_name in cls._BOUND)
            if len(sizes) != 1:
                msg = "Size mismatch of arrays in {}: {}"
                raise ProphyError(msg.format(parent.__class__.__name__, ", ".join(cls._BOUND)))
            return sizes.pop()

        @staticmethod
        def _encode(value, endianness):
            return sizer_item_type._encode(value + bound_shift, endianness)

        @staticmethod
        def _decode(data, pos, endianness):
            value, size = sizer_item_type._decode(data, pos, endianness)
            array_guard = 65536
            if value > array_guard:
                raise ProphyError("decoded array length over %s" % array_guard)
            value -= bound_shift
            if value < 0:
                raise ProphyError("decoded array length smaller than shift")
            return value, size

        @classmethod
        def _bricks(cls):
            yield sizer_item_type, None

    return container_len


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
        return (type_._optional_type._encode(True, endianness).ljust(type_._OPTIONAL_ALIGNMENT, b'\x00') +
                type_._encode(parent, type_.__bases__[0], value, endianness))


def encode_array_delimiter(parent, type_, value, endianness):
    return type_._encode(type_.evaluate(parent), endianness)


def encode_array(parent, type_, value, endianness):
    return value._encode_impl(endianness)


def encode_composite(parent, type_, value, endianness):
    return value.encode(endianness, terminal=False)


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
        return type_._OPTIONAL_ALIGNMENT + type_._decode(parent, name, type_.__bases__[0],
                                                         data, pos + type_._OPTIONAL_ALIGNMENT, endianness,
                                                         len_hints)
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


def decode_array(parent, name, _, data, pos, endianness, len_hints):
    return getattr(parent, name)._decode_impl(data, pos, endianness, len_hints.get(name))


def decode_composite(parent, name, _, data, pos, endianness, __):
    return getattr(parent, name)._decode_impl(data, pos, endianness, terminal=False)


def decode_bytes(parent, name, type_, data, pos, _, len_hints):
    value, size = type_._decode(data, pos, len_hints.get(name))
    setattr(parent, name, value)
    return size


def decode_scalar(parent, name, type_, data, pos, endianness, _):
    value, size = type_._decode(data, pos, endianness)
    setattr(parent, name, value)
    return size


def indent(text, spaces):
    return '\n'.join(x and spaces * ' ' + x or '' for x in text.split('\n'))


def field_to_string(name, type_, value):
    if issubclass(type_, base_array):
        return "".join(field_to_string(name, type_._TYPE, elem) for elem in value)
    elif issubclass(type_, (struct, union)):
        return "%s {\n%s}\n" % (name, indent(str(value), spaces=2))
    elif issubclass(type_, bytes):
        return "%s: %s\n" % (name, repr_bytes(value))
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
        def to_str(item):
            value = getattr(self, item.name, None)
            return field_to_string(item.name, item.type, value) if value is not None else ""
        return "".join(to_str(i) for i in self._descriptor)

    @classmethod
    def get_descriptor(cls):
        return [FieldDescriptor(item.name, item.type, get_kind(item.type)) for item in cls._descriptor]

    @classmethod
    def _get_padding(cls, offset, alignment):
        return b'\x00' * cls._get_padding_size(offset, alignment)

    @staticmethod
    def _get_padding_size(offset, alignment):
        return distance_to_next_multiply(offset, alignment)

    @classmethod
    def _wire_walk(cls):
        data = ""
        for item in cls._descriptor:
            data += (cls._get_padding(len(data), item.type._ALIGNMENT))
            data += item.encode_fcn(cls, item.type, getattr(cls, item.name, None), endianness)

            if item.type._PARTIAL_ALIGNMENT:
                data += cls._get_padding(len(data), item.type._PARTIAL_ALIGNMENT)

        data += cls._get_padding(len(data), cls._ALIGNMENT)

    def encode(self, endianness, terminal=True):
        data = b""

        for item in self._descriptor:
            data += (self._get_padding(len(data), item.type._ALIGNMENT))
            data += item.encode_fcn(self, item.type, getattr(self, item.name, None), endianness)

            if item.type._PARTIAL_ALIGNMENT:
                data += self._get_padding(len(data), item.type._PARTIAL_ALIGNMENT)

        data += self._get_padding(len(data), self._ALIGNMENT)

        return data

    def decode(self, data, endianness):
        return self._decode_impl(data, 0, endianness, terminal=True)

    def _decode_impl(self, data, pos, endianness, terminal):
        len_hints = {}
        start_pos = pos

        for item in self._descriptor:
            pos += self._get_padding_size(pos, item.type._ALIGNMENT)
            try:
                pos += item.decode_fcn(self, item.name, item.type, data, pos, endianness, len_hints)
            except ProphyError as e:
                raise ProphyError("{}: {}".format(self.__class__.__name__, e))
            if item.type._PARTIAL_ALIGNMENT:
                pos += self._get_padding_size(pos, item.type._PARTIAL_ALIGNMENT)

        pos += self._get_padding_size(pos, self._ALIGNMENT)

        if terminal and pos < len(data):
            raise ProphyError("not all bytes of {} read".format(self.__class__.__name__))

        return pos - start_pos

    def copy_from(self, other):
        validate_copy_from(self, other)
        if other is self:
            return

        self._fields.clear()
        for name, rhs in other._fields.items():
            set_field(self, name, rhs)

    @classmethod
    def _bricks(cls):
        for name, type_, _, _ in cls._descriptor:
            for brick_type, brick_path in type_._bricks():
                path_ = ".%s" % name
                if brick_path is not None:
                    path_ += brick_path
                yield brick_type, path_

    @classmethod
    def wire_stamp(cls):
        def collect():
            for type_, path_ in cls._bricks():
                type_size = getattr(type_, "_SIZE", "??")
                yield "%s (%s) [%s];\n" % (path_, type_.__name__, type_size)

        return "".join(collect())


class struct_packed(struct):
    __slots__ = []

    @staticmethod
    def _get_padding_size(_, __):
        return 0


class composite_generator_base(type):
    _slots = []
    _descriptor_item_type = None

    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = cls._slots
        return super(composite_generator_base, cls).__new__(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        if not hasattr(self, "_generated"):
            self._generated = True
            self._descriptor = [self._descriptor_item_type(*item) for item in self._descriptor]
            self.validate()
            self.add_attributes()
            self.extend_descriptor()
            self.add_properties()
            self.add_sizers()
        super(composite_generator_base, self).__init__(name, bases, attrs)

    def _types(self):
        for item in self._descriptor:
            yield item.type

    def add_sizers(self):
        pass

    def extend_descriptor(self):
        for i, raw_item in enumerate(self._descriptor):
            self._descriptor[i] = raw_item._add_codecs()


class struct_generator(composite_generator_base):
    _slots = ["_fields"]
    _descriptor_item_type = RawStructItem

    def validate(self):
        for type_ in list(self._types())[:-1]:
            if type_._UNLIMITED:
                raise ProphyError("unlimited field is not the last one")

    def add_attributes(self):
        self._BOUND = None
        self._DYNAMIC = any(type_._DYNAMIC for type_ in self._types())
        self._OPTIONAL = False
        self._PARTIAL_ALIGNMENT = None
        self._SIZE = sum((type_._OPTIONAL_SIZE if type_._OPTIONAL else type_._SIZE) for type_ in self._types())
        self._UNLIMITED = any(type_._UNLIMITED for type_ in self._types())
        if not self._descriptor:
            self._ALIGNMENT = 1
        else:
            self._ALIGNMENT = max((t._OPTIONAL_ALIGNMENT if t._OPTIONAL else t._ALIGNMENT) for t in self._types())

        alignment = 1
        for type_ in reversed(list(self._types())):
            if issubclass(type_, (base_array, bytes)) and type_._DYNAMIC:
                type_._PARTIAL_ALIGNMENT = alignment
                alignment = 1
            alignment = max(type_._ALIGNMENT, alignment)
        if not issubclass(self, struct_packed) and self._descriptor:
            self._SIZE += sum(self.get_padded_sizes())

    def get_padded_sizes(self):
        types = list(self._types())
        sizes = [tp._SIZE for tp in types]
        alignments = [tp._ALIGNMENT for tp in types[1:]] + [self._ALIGNMENT]
        offset = 0

        for size, alignment in zip(sizes, alignments):
            offset += size
            padding = distance_to_next_multiply(offset, alignment)
            offset += padding
            yield padding

    def add_properties(self):
        for item in self._descriptor:
            if issubclass(item.type, base_array):
                self.add_repeated(item)
            elif issubclass(item.type, (struct, union)):
                self.add_composite(item)
            else:
                self.add_scalar(item)

    def add_sizers(self):
        for item in self._descriptor:
            if issubclass(item.type, base_array) or not issubclass(item.type, (struct, union)):
                if item.type._BOUND:
                    self.substitute_len_field(item)

    def add_repeated(self, descriptor_item):
        def getter(self_):
            value = self_._fields.get(descriptor_item.name)
            if value is None:
                value = descriptor_item.type()
                self_._fields[descriptor_item.name] = value
            return value

        def setter(self_, new_value):
            raise ProphyError("assignment to array field not allowed")

        setattr(self, descriptor_item.name, property(getter, setter))

#         if descriptor_item.type._BOUND:
#             self.substitute_len_field(descriptor_item)

    def add_scalar(self, descriptor_item):
        if descriptor_item.type._OPTIONAL:
            def getter(self_):
                return self_._fields.get(descriptor_item.name)

            def setter(self_, new_value):
                if new_value is None:
                    self_._fields[descriptor_item.name] = None
                else:
                    self_._fields[descriptor_item.name] = descriptor_item.type._check(new_value)
        else:
            def getter(self_):
                return self_._fields.get(descriptor_item.name, descriptor_item.type._DEFAULT)

            def setter(self_, new_value):
                self_._fields[descriptor_item.name] = descriptor_item.type._check(new_value)
        setattr(self, descriptor_item.name, property(getter, setter))
#         if descriptor_item.type._BOUND:
#             self.substitute_len_field(descriptor_item)

    def add_composite(self, descriptor_item):
        if descriptor_item.type._OPTIONAL:
            def getter(self_):
                return self_._fields.get(descriptor_item.name)

            def setter(self_, new_value):
                if new_value is True:
                    self_._fields[descriptor_item.name] = descriptor_item.type()
                elif new_value is None:
                    self_._fields.pop(descriptor_item.name, None)
                else:
                    raise ProphyError("assignment to composite field not allowed")
        else:
            def getter(self_):
                value = self_._fields.get(descriptor_item.name)
                if value:
                    return value
                else:
                    return self_._fields.setdefault(descriptor_item.name, descriptor_item.type())

            def setter(self_, new_value):
                raise ProphyError("assignment to composite field not allowed")
        setattr(self, descriptor_item.name, property(getter, setter))

    def substitute_len_field(self, container_item):
        sizer_name = self.validate_and_fix_sizer_name(container_item)
        index, sizer_item = next((index, f) for index, f in enumerate(self._descriptor) if f.name == sizer_name)
        bound_shift = container_item.type._BOUND_SHIFT
        self.validate_sizer_type(sizer_item, container_item)

        if sizer_item.type.__name__ == "container_len":
            " sizer already created for other container "
            sizer_item.type.add_bounded_container(container_item.name)
            self.validate_bound_shift(sizer_item.type, container_item.name, bound_shift)

        else:
            container_len_class = build_container_length_field(sizer_item.type, container_item.name, bound_shift)
            raw_item = RawStructItem(sizer_item.name, container_len_class)
            self._descriptor[index] = raw_item._add_codecs()
            delattr(self, sizer_item.name)

    def validate_and_fix_sizer_name(self, container_item):
        sizer_name = container_item.type._BOUND
        all_names = [item.name for item in self._descriptor]

        if sizer_name not in all_names:
            msg = "Sizing member '{}' of container '{}' not found in the object '{}'."
            msg = msg.format(sizer_name, container_item.name, self.__name__)

            """ Try to be lenient. """
            if (sizer_name + 's') in all_names:
                sizer_name += 's'

            elif sizer_name.endswith('s') and sizer_name[:-1] in all_names:
                sizer_name = sizer_name[:-1]

            elif len([n for n in all_names if n.startswith("numOf")]) == 1:
                if len([f for f in self._descriptor if f.type._BOUND]) == 1:
                    """ If there is one sizer and only one array. """
                    sizer_name = next(f for f in self._descriptor if f.name.startswith("numOf")).name
            else:
                raise ProphyError(msg)

            container_item.type._BOUND = sizer_name
            msg = "Warning: {}\n Picking '{}' as the missing sizer instead.\n".format(msg, sizer_name)
            print(msg)

        return sizer_name

    def validate_sizer_type(self, sizer_item, container_item):
        if sizer_item.type._OPTIONAL:
            msg = "array {}.{} must not be bound to optional field"
            raise ProphyError(msg.format(self.__name__, container_item.name))
        if not issubclass(sizer_item.type, (int, long)):
            msg = "array {}.{} must be bound to an unsigned integer"
            raise ProphyError(msg.format(self.__name__, container_item.name))

    def validate_bound_shift(self, sizer_item_type, container_name, expected_bound_shift):
        msg = "Different bound shifts are unsupported in externally sized arrays ({}.{})"
        for item in self._descriptor:
            if item.name in sizer_item_type._BOUND:
                if not item.type._BOUND_SHIFT == expected_bound_shift:
                    raise ProphyError(msg.format(self.__name__, container_name))


def get_discriminated_field(cls, discriminator):
    for item in cls._descriptor:
        if item.discriminator == discriminator:
            return item
    raise ProphyError("unknown discriminator: {!r}".format(discriminator))


class union(object):
    __slots__ = []

    def __init__(self):
        self._fields = {}
        self._discriminated = self._descriptor[0]

    def __str__(self):
        name = self._discriminated.name
        value = getattr(self, name)
        return field_to_string(name, self._discriminated.type, value)

    def get_discriminated(self):
        name, tp = self._discriminated[:2]
        return FieldDescriptor(name, tp, get_kind(tp))

    @classmethod
    def get_descriptor(cls):
        return [FieldDescriptor(item.name, item.type, get_kind(item.type)) for item in cls._descriptor]

    def encode(self, endianness, terminal=True):
        name, tp, disc, encode_, _ = self._discriminated
        value = getattr(self, name)
        return (
            self._discriminator_type._encode(disc, endianness).ljust(self._ALIGNMENT, b'\x00') +
            encode_(self, tp, value, endianness)
        ).ljust(self._SIZE, b'\x00')

    def decode(self, data, endianness):
        return self._decode_impl(data, 0, endianness, terminal=True)

    def _decode_impl(self, data, pos, endianness, terminal):
        disc, _ = self._discriminator_type._decode(data, pos, endianness)
        item = get_discriminated_field(self, disc)

        self._discriminated = item
        item.decode_fcn(self, item.name, item.type, data, pos + self._ALIGNMENT, endianness, {})
        if (len(data) - pos) < self._SIZE:
            raise ProphyError("not enough bytes")
        if terminal and (len(data) - pos) > self._SIZE:
            raise ProphyError("not all bytes of {} read".format(self.__class__.__name__))
        return self._SIZE

    def copy_from(self, other):
        validate_copy_from(self, other)
        if other is self:
            return

        self._fields.clear()
        self._discriminated = other._discriminated
        rhs = getattr(other, self._discriminated.name)
        if issubclass(self._discriminated.type, (struct, union)):
            lhs = getattr(self, self._discriminated.name)
            lhs.copy_from(rhs)
        else:
            setattr(self, self._discriminated.name, rhs)


class union_generator(composite_generator_base):
    _slots = ["_fields", "_discriminated"]
    _descriptor_item_type = RawUnionItem

    def validate(self):
        for type_ in self._types():
            if type_._DYNAMIC:
                raise ProphyError("dynamic types not allowed in union")
            if type_._BOUND:
                raise ProphyError("bound array/bytes not allowed in union")
            if issubclass(type_, base_array):
                raise ProphyError("static array not implemented in union")
            if type_._OPTIONAL:
                raise ProphyError("union with optional field disallowed")

    def add_attributes(self):
        self._ALIGNMENT = max(scalar.u32._ALIGNMENT, max(type_._ALIGNMENT for type_ in self._types()))
        self._BOUND = None
        self._DYNAMIC = False
        self._OPTIONAL = False
        self._PARTIAL_ALIGNMENT = None
        unaligned_size = self._ALIGNMENT + max(type_._SIZE for type_ in self._types())
        self._SIZE = unaligned_size + distance_to_next_multiply(unaligned_size, self._ALIGNMENT)
        self._UNLIMITED = False
        self._discriminator_type = scalar.u32

    def add_properties(self):
        self.add_union_discriminator()
        for item in self._descriptor:
            if issubclass(item.type, (struct, union)):
                self.add_union_composite(item)
            else:
                self.add_union_scalar(item)

    def add_union_discriminator(self):
        def getter(self_):
            return self_._discriminated[2]

        def setter(self_, discriminator_name_or_value):
            for item in self_._descriptor:
                if discriminator_name_or_value in (item.name, item.discriminator):
                    if item != self_._discriminated:
                        self_._discriminated = item
                        self_._fields = {}
                    return
            raise ProphyError("unknown discriminator: {!r}".format(discriminator_name_or_value))

        setattr(self, "discriminator", property(getter, setter))

    def add_union_composite(self, item):
        def getter(self_):
            if self_._discriminated is not item:
                raise ProphyError("currently field %s is discriminated" % self_._discriminated[2])
            value = self_._fields.get(item.name)
            if value is None:
                value = item.type()
                value = self_._fields.setdefault(item.name, value)
            return value

        def setter(self_, new_value):
            raise ProphyError("assignment to composite field not allowed")
        setattr(self, item.name, property(getter, setter))

    def add_union_scalar(self, item):
        def getter(self_):
            if self_._discriminated is not item:
                raise ProphyError("currently field %s is discriminated" % self_._discriminated[2])
            return self_._fields.get(item.name, item.type._DEFAULT)

        def setter(self_, new_value):
            if self_._discriminated is not item:
                raise ProphyError("currently field %s is discriminated" % self_._discriminated[2])
            new_value = item.type._check(new_value)
            self_._fields[item.name] = new_value
        setattr(self, item.name, property(getter, setter))


class FieldDescriptor(object):
    def __init__(self, name, type_, kind):
        self.name = name
        self.type = type_
        self.kind = kind

    def __repr__(self):
        return ("<{}, {!r}, {!r}>".format(self.name, self.type, self.kind))
