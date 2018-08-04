from collections import namedtuple

from . import scalar
from .base_array import base_array
from .exception import ProphyError
from .six import long, repr_bytes, string_types
from .base import kind, prophy_data_object


FieldDescriptor = namedtuple("FieldDescriptor", "name, type, kind")
FieldDescriptor.__repr__ = lambda self: "<{}, {!r}, {!r}>".format(*self)


class codec_kind(object):
    OPTIONAL = "OPTIONAL"
    ARRAY_SIZER = "ARRAY_SIZER"
    ARRAY = "ARRAY"
    COMPOSITE = "COMPOSITE"
    BYTES = "BYTES"
    SCALAR = "SCALAR"

    @classmethod
    def classify(cls, type_):
        if type_._OPTIONAL:
            return cls.OPTIONAL
        elif type_._BOUND and issubclass(type_, (int, long)):
            return cls.ARRAY_SIZER
        elif issubclass(type_, base_array):
            return cls.ARRAY
        elif issubclass(type_, (struct, union)):
            return cls.COMPOSITE
        elif issubclass(type_, bytes):
            return cls.BYTES
        else:
            return cls.SCALAR


class _cursor_class(object):
    def __init__(self):
        self.pos = 0

    def distance_to_next(self, alignment):
        remainer = self.pos % alignment
        return (alignment - remainer) % alignment

    def move_to_next(self, alignment):
        self.pos += distance_to_next_multiply(self.pos, alignment)


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
        def evaluate_size(cls, parent):
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
        def _bricks_walk(cls, _):
            yield sizer_item_type, " (sizer)"

    return container_len


class descriptor_item_type(object):
    __slots__ = ["name", "type", "discriminator", "encode_fcn", "decode_fcn"]

    def __init__(self, name, type_, discriminator=None):
        self.name = name
        self.type = type_
        self.discriminator = discriminator
        self.encode_fcn = None
        self.decode_fcn = None

    def __repr__(self):
        is_union_descriptor = self.discriminator is not None
        if is_union_descriptor:
            return "{}({!r}, {!r}, {!r})".format(type(self).__name__, self.name, self.type, self.discriminator)
        else:
            return "{}({!r}, {!r})".format(type(self).__name__, self.name, self.type)

    def evaluate_codecs(self):
        all_codecs = {
            codec_kind.OPTIONAL: (encode_optional, decode_optional),
            codec_kind.ARRAY_SIZER: (encode_array_delimiter, decode_array_delimiter),
            codec_kind.ARRAY: (encode_array, decode_array),
            codec_kind.COMPOSITE: (encode_composite, decode_composite),
            codec_kind.BYTES: (encode_bytes, decode_bytes),
            codec_kind.SCALAR: (encode_scalar, decode_scalar)
        }
        kind = codec_kind.classify(self.type)
        assert kind in all_codecs
        self.encode_fcn, self.decode_fcn = all_codecs.get(kind)

        if kind == codec_kind.OPTIONAL:
            base_kind = codec_kind.classify(self.type.__bases__[0])
            opt_encode, opt_decode = all_codecs.get(base_kind)

            self.type._encode = staticmethod(opt_encode)
            self.type._decode = staticmethod(opt_decode)

    @property
    def kind(self):
        if issubclass(self.type, base_array):
            return kind.ARRAY
        elif issubclass(self.type, struct):
            return kind.STRUCT
        elif issubclass(self.type, union):
            return kind.UNION
        elif issubclass(self.type, bytes):
            return kind.BYTES
        elif issubclass(self.type, scalar.enum):
            return kind.ENUM
        else:
            return kind.INT

    @property
    def descriptor_info(self):
        return FieldDescriptor(self.name, self.type, self.kind)


def encode_optional(parent, type_, value, endianness):
    if value is None:
        return b"\x00" * type_._OPTIONAL_SIZE
    else:
        return (type_._optional_type._encode(True, endianness).ljust(type_._OPTIONAL_ALIGNMENT, b'\x00') +
                type_._encode(parent, type_.__bases__[0], value, endianness))


def encode_array_delimiter(parent, type_, _, endianness):
    return type_._encode(type_.evaluate_size(parent), endianness)


def encode_array(_, __, value, endianness):
    return value._encode_impl(endianness)


def encode_composite(_, __, value, endianness):
    return value.encode(endianness)


def encode_bytes(_, type_, value, __):
    return type_._encode(value)


def encode_scalar(_, type_, value, endianness):
    return type_._encode(value, endianness)


def decode_optional(parent, name, type_, data, pos, endianness, len_hints):
    value, _ = type_._optional_type._decode(data, pos, endianness)
    opt_alignment = type_._OPTIONAL_ALIGNMENT
    if value:
        setattr(parent, name, True)
        sub_type = type_.__bases__[0]
        pos += opt_alignment
        return opt_alignment + type_._decode(parent, name, sub_type, data, pos, endianness, len_hints)
    else:
        setattr(parent, name, None)
        return opt_alignment + type_._SIZE


def decode_array_delimiter(_, __, type_, data, pos, endianness, len_hints):
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


def make_padding(padding_size):
    class PaddingMock(object):
        _SIZE = padding_size

        @staticmethod
        def encode_mock():
            return b'\x00' * padding_size

        @staticmethod
        def decode_mock(data, pos):
            if (len(data) - pos) < padding_size:
                raise ProphyError("too few bytes to decode padding")
            return data[pos:(pos + padding_size)], padding_size
    PaddingMock.__name__ = "<Pd{}>".format(padding_size)
    return PaddingMock


def field_to_string(name, type_, value):
    single_indent_level = " " * 2

    def indent(text):
        return '\n'.join(x and single_indent_level + x or '' for x in text.split('\n'))

    if issubclass(type_, base_array):
        return "".join(field_to_string(name, type_._TYPE, elem) for elem in value)
    elif issubclass(type_, (struct, union)):
        return "%s {\n%s}\n" % (name, indent(str(value)))
    elif issubclass(type_, bytes):
        return "%s: %s\n" % (name, repr_bytes(value))
    elif issubclass(type_, scalar.enum):
        return "%s: %s\n" % (name, type_._int_to_name[value])
    else:
        return "%s: %s\n" % (name, value)


def validate_copy_from(lhs, rhs):
    if not isinstance(rhs, lhs.__class__):
        raise TypeError("Parameter to copy_from must be instance of same class.")


def eval_path(node_path, leaf_path):
    return ".%s%s" % (node_path, leaf_path or "")


class struct(prophy_data_object):
    __slots__ = []

    def __init__(self):
        self._fields = {}

    def __str__(self):
        def to_str():
            for item in self._descriptor:
                value = getattr(self, item.name, None)
                if value is not None:
                    yield field_to_string(item.name, item.type, value)

        return "".join(to_str())

    @classmethod
    def get_descriptor(cls):
        """
            FIXME: I'm afraid it rapes YAGNI rule
        """
        return [item.descriptor_info for item in cls._descriptor]

    @classmethod
    def _get_padding(cls, offset, alignment):
        return b'\x00' * cls._get_padding_size(offset, alignment)

    @staticmethod
    def _get_padding_size(offset, alignment):
        return distance_to_next_multiply(offset, alignment)

    def encode(self, endianness):
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
        """ TODO: method common to struct and union. """
        validate_copy_from(self, other)
        if other is self:
            return

        self._fields.clear()
        self._copy_implementation(other)

    def _copy_implementation(self, other):
        for name, rhs in other._fields.items():
            self.set_field(name, rhs)

    def set_field(self, name, rhs):
        lhs = getattr(self, name)
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
            self._fields[name] = rhs

    @classmethod
    def wire_pattern(cls):

        cursor = _cursor_class()
        for type_, path_ in cls._bricks_walk(cursor):
            type_size = getattr(type_, "_SIZE", "??")
            if type_size != "??":
                cursor.pos += type_size
            yield path_, type_.__name__, type_size




class struct_packed(struct):
    __slots__ = []

    @staticmethod
    def _get_padding_size(_, __):
        return 0


class composite_generator_base(type):
    _slots = []

    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = cls._slots
        return super(composite_generator_base, cls).__new__(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        if not hasattr(self, "_generated"):
            self._generated = True
            self._descriptor = [descriptor_item_type(*item) for item in self._descriptor]
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
        for raw_item in self._descriptor:
            raw_item.evaluate_codecs()

    def _bricks_walk(self, cursor):
        for item in self._descriptor:
            padding_size = cursor.distance_to_next(item.type._ALIGNMENT)
            if padding_size:
                yield make_padding(padding_size), eval_path(item.name, ".:pre_padding")

            for sub_brick_type, sub_brick_path in item.type._bricks_walk(cursor):
                yield sub_brick_type, eval_path(item.name, sub_brick_path)

            if item.type._PARTIAL_ALIGNMENT:
                padding_size = cursor.distance_to_next(item.type._PARTIAL_ALIGNMENT)
                if padding_size:
                    yield make_padding(padding_size), eval_path(item.name, ".:partial_padding")

        padding_size = cursor.distance_to_next(self._ALIGNMENT)
        if padding_size:
            yield make_padding(padding_size), eval_path(item.name, ".:final_padding")

    def get_descriptor(self):
        """
            FIXME: I'm afraid it rapes YAGNI rule
        """
        return [item.descriptor_info for item in self._descriptor]


class struct_generator(composite_generator_base):
    _slots = ["_fields"]

    def validate(self):
        for item in self._descriptor:
            if not isinstance(item.name, string_types):
                raise ProphyError("member name must be a string type")
            if not hasattr(item.type, "_is_prophy_object"):
                raise ProphyError("member type must be a prophy object, is: {!r}".format(item.type))

        types = list(self._types())
        for type_ in types[:-1]:
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
                self.add_repeated_property(item)
            elif issubclass(item.type, (struct, union)):
                self.add_composite_property(item)
            else:
                self.add_scalar_property(item)

    def add_sizers(self):
        for item in self._descriptor:
            if issubclass(item.type, base_array) or not issubclass(item.type, (struct, union)):
                if item.type._BOUND:
                    self.substitute_len_field(item)

    def add_repeated_property(self, descriptor_item):
        def getter(self_):
            value = self_._fields.get(descriptor_item.name)
            if value is None:
                value = descriptor_item.type()
                self_._fields[descriptor_item.name] = value
            return value

        def setter(self_, new_value):
            raise ProphyError("assignment to array field not allowed")

        setattr(self, descriptor_item.name, property(getter, setter))

    def add_scalar_property(self, descriptor_item):
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

    def add_composite_property(self, descriptor_item):
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
        sizer_item = next(item for item in self._descriptor if item.name == sizer_name)
        bound_shift = container_item.type._BOUND_SHIFT
        self.validate_sizer_type(sizer_item, container_item)

        if sizer_item.type.__name__ == "container_len":
            sizer_item.type.add_bounded_container(container_item.name)
            self.validate_bound_shift(sizer_item.type, container_item.name, bound_shift)

        else:
            sizer_item.type = build_container_length_field(sizer_item.type, container_item.name, bound_shift)
            sizer_item.evaluate_codecs()
            delattr(self, sizer_item.name)

    def validate_and_fix_sizer_name(self, container_item):
        sizer_name = container_item.type._BOUND
        items_before_sizer = self._descriptor[:self._descriptor.index(container_item)]
        all_names = [item.name for item in self._descriptor]
        names_before = [item.name for item in items_before_sizer]

        if sizer_name not in names_before:
            if sizer_name in all_names:
                msg = "Sizing member '{}' in '{}' must be placed before '{}' container."
                raise ProphyError(msg.format(sizer_name, self.__name__, container_item.name))

            msg = "Sizing member '{}' of container '{}' not found in the object '{}'."
            msg = msg.format(sizer_name, container_item.name, self.__name__)

            """ Try to be lenient. """
            there_is_sizer_ending_with_s = (sizer_name + 's') in names_before
            there_is_sizer_without_s = sizer_name.endswith('s') and sizer_name[:-1] in names_before
            there_is_exactly_one_sizer = len([n for n in names_before if n.startswith("numOf")]) == 1
            there_is_one_bound_array = len([f for f in self._descriptor if f.type._BOUND]) == 1

            if there_is_sizer_ending_with_s:
                sizer_name += 's'

            elif there_is_sizer_without_s:
                sizer_name = sizer_name[:-1]

            elif there_is_exactly_one_sizer and there_is_one_bound_array:
                sizer_name = next(f for f in items_before_sizer if f.name.startswith("numOf")).name
            else:
                raise ProphyError(msg)

            container_item.type._BOUND = sizer_name
            print("Warning: {}\n Picking '{}' as the missing sizer instead.\n".format(msg, sizer_name))

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


class union(prophy_data_object):
    __slots__ = []

    def __init__(self):
        self._fields = {}
        self._discriminated = self._descriptor[0]

    def __str__(self):
        name = self._discriminated.name
        value = getattr(self, name)
        return field_to_string(name, self._discriminated.type, value)

    def get_discriminated(self):
        """
            FIXME: I'm afraid it rapes YAGNI rule
        """
        return self._discriminated.descriptor_info

    def encode(self, endianness, **_):
        d = self._discriminated
        value = getattr(self, d.name)
        discriminator_bytes = self._discriminator_type._encode(d.discriminator, endianness).ljust(self._ALIGNMENT, b'\x00')
        body_bytes = d.encode_fcn(self, d.type, value, endianness)
        return (discriminator_bytes + body_bytes).ljust(self._SIZE, b'\x00')

    def decode(self, data, endianness):
        return self._decode_impl(data, 0, endianness, terminal=True)

    def _decode_impl(self, data, pos, endianness, terminal):
        disc, _ = self._discriminator_type._decode(data, pos, endianness)
        item = self._get_discriminated_field(disc)

        self._discriminated = item
        item.decode_fcn(self, item.name, item.type, data, pos + self._ALIGNMENT, endianness, {})

        bytes_read = len(data) - pos
        if bytes_read < self._SIZE:
            raise ProphyError("not enough bytes")
        if terminal and bytes_read > self._SIZE:
            raise ProphyError("not all bytes of {} read".format(self.__class__.__name__))
        return self._SIZE

    def _get_discriminated_field(self, discriminator):
        for item in self._descriptor:
            if item.discriminator == discriminator:
                return item
        raise ProphyError("unknown discriminator: {!r}".format(discriminator))

    def copy_from(self, other):
        """ TODO: method common to struct and union. """
        validate_copy_from(self, other)
        if other is self:
            return

        self._fields.clear()
        self._copy_implementation(other)

    def _copy_implementation(self, other):
        self._discriminated = other._discriminated
        rhs = getattr(other, self._discriminated.name)
        if issubclass(self._discriminated.type, (struct, union)):
            lhs = getattr(self, self._discriminated.name)
            lhs.copy_from(rhs)
        else:
            setattr(self, self._discriminated.name, rhs)


class union_generator(composite_generator_base):
    _slots = ["_fields", "_discriminated"]

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
        natural_size = self._ALIGNMENT + max(type_._SIZE for type_ in self._types())
        self._SIZE = natural_size + distance_to_next_multiply(natural_size, self._ALIGNMENT)
        self._UNLIMITED = False
        self._discriminator_type = scalar.u32

    def add_properties(self):
        self.add_union_discriminator_property()
        for item in self._descriptor:
            if issubclass(item.type, (struct, union)):
                self.add_union_composite_property(item)
            else:
                self.add_union_scalar_property(item)

    def add_union_discriminator_property(self):
        def getter(self_):
            return self_._discriminated.discriminator

        def setter(self_, discriminator_name_or_value):
            for item in self_._descriptor:
                if discriminator_name_or_value in (item.name, item.discriminator):
                    if item != self_._discriminated:
                        self_._discriminated = item
                        self_._fields = {}
                    return
            raise ProphyError("unknown discriminator: {!r}".format(discriminator_name_or_value))

        setattr(self, "discriminator", property(getter, setter))

    def add_union_composite_property(self, item):
        def getter(self_):
            if self_._discriminated is not item:
                raise ProphyError("currently field %s is discriminated" % self_._discriminated.discriminator)
            value = self_._fields.get(item.name)
            if value is None:
                value = item.type()
                value = self_._fields.setdefault(item.name, value)
            return value

        def setter(self_, new_value):
            raise ProphyError("assignment to composite field not allowed")
        setattr(self, item.name, property(getter, setter))

    def add_union_scalar_property(self, item):
        def getter(self_):
            if self_._discriminated is not item:
                raise ProphyError("currently field %s is discriminated" % self_._discriminated.discriminator)
            return self_._fields.get(item.name, item.type._DEFAULT)

        def setter(self_, new_value):
            if self_._discriminated is not item:
                raise ProphyError("currently field %s is discriminated" % self_._discriminated.discriminator)
            new_value = item.type._check(new_value)
            self_._fields[item.name] = new_value
        setattr(self, item.name, property(getter, setter))
