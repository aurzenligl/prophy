from .base_array import base_array
from .composite_base import _composite_base
from .exception import ProphyError
from .scalar import enum
from .six import repr_bytes, long


def distance_to_next_multiply(number, alignment):
    remainer = number % alignment
    return (alignment - remainer) % alignment


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
    elif issubclass(type_, enum):
        return "%s: %s\n" % (name, type_._int_to_name[value])
    else:
        return "%s: %s\n" % (name, value)


class struct(_composite_base):
    _padding_byte = b'\x00'
    __slots__ = []

    def __init__(self):
        self._fields = {}

    def __str__(self):
        def to_str():
            for field in self._descriptor:
                value = getattr(self, field.name, None)
                if value is not None:
                    yield field_to_string(field.name, field.type, value)

        return "".join(to_str())

    @classmethod
    def get_descriptor(cls):
        return [field.descriptor_info for field in cls._descriptor]

    @classmethod
    def _get_padding(cls, offset, alignment):
        return cls._padding_byte * cls._get_padding_size(offset, alignment)

    @staticmethod
    def _get_padding_size(offset, alignment):
        return distance_to_next_multiply(offset, alignment)

    def encode(self, endianness):
        data = b""

        for field in self._descriptor:
            data += (self._get_padding(len(data), field.type._ALIGNMENT))
            data += field.encode_fcn(self, field.type, getattr(self, field.name, None), endianness)

            if field.type._PARTIAL_ALIGNMENT:
                data += self._get_padding(len(data), field.type._PARTIAL_ALIGNMENT)

        data += self._get_padding(len(data), self._ALIGNMENT)

        return data

    def decode(self, data, endianness):
        return self._decode_impl(data, 0, endianness, terminal=True)

    def _decode_impl(self, data, pos, endianness, terminal):
        len_hints = {}
        start_pos = pos

        for field in self._descriptor:
            pos += self._get_padding_size(pos, field.type._ALIGNMENT)
            try:
                pos += field.decode_fcn(self, field.name, field.type, data, pos, endianness, len_hints)
            except ProphyError as e:
                raise ProphyError("{}: {}".format(self.__class__.__name__, e))
            if field.type._PARTIAL_ALIGNMENT:
                pos += self._get_padding_size(pos, field.type._PARTIAL_ALIGNMENT)

        pos += self._get_padding_size(pos, self._ALIGNMENT)

        if terminal and pos < len(data):
            raise ProphyError("not all bytes of {} read".format(self.__class__.__name__))

        return pos - start_pos

    def _copy_implementation(self, other):
        for name, rhs in other._fields.items():
            self.set_field(name, rhs)

    def set_field(self, name, rhs):
        lhs = getattr(self, name)
        if isinstance(rhs, base_array):
            if codec_kind.is_composite(rhs._TYPE):
                if rhs._DYNAMIC:
                    del lhs[:]
                    lhs.extend(rhs[:])
                else:
                    for lhs_elem, rhs_elem in zip(lhs, rhs):
                        lhs_elem.copy_from(rhs_elem)
            else:
                lhs[:] = rhs[:]
        elif codec_kind.is_composite(type(rhs)):
            lhs.copy_from(rhs)
        else:
            self._fields[name] = rhs


class struct_packed(struct):
    __slots__ = []

    @staticmethod
    def _get_padding_size(_, __):
        return 0


class union(_composite_base):
    __slots__ = []

    def __init__(self):
        self._fields = {}
        self._discriminated = self._descriptor[0]

    def __str__(self):
        name = self._discriminated.name
        value = getattr(self, name)
        return field_to_string(name, self._discriminated.type, value)

    def get_discriminated(self):
        return self._discriminated.descriptor_info

    def encode(self, endianness, **_):
        d = self._discriminated
        value = getattr(self, d.name)
        discriminator_bytes = self._discriminator_type._encode(
            d.discriminator, endianness).ljust(self._ALIGNMENT, b'\x00')
        body_bytes = d.encode_fcn(self, d.type, value, endianness)
        return (discriminator_bytes + body_bytes).ljust(self._SIZE, b'\x00')

    def decode(self, data, endianness):
        return self._decode_impl(data, 0, endianness, terminal=True)

    def _decode_impl(self, data, pos, endianness, terminal):
        disc, _ = self._discriminator_type._decode(data, pos, endianness)
        field = self._get_discriminated_field(disc)

        self._discriminated = field
        field.decode_fcn(self, field.name, field.type, data, pos + self._ALIGNMENT, endianness, {})

        bytes_read = len(data) - pos
        if bytes_read < self._SIZE:
            raise ProphyError("not enough bytes")
        if terminal and bytes_read > self._SIZE:
            raise ProphyError("not all bytes of {} read".format(self.__class__.__name__))
        return self._SIZE

    def _get_discriminated_field(self, discriminator):
        for field in self._descriptor:
            if field.discriminator == discriminator:
                return field
        raise ProphyError("unknown discriminator: {!r}".format(discriminator))

    def _copy_implementation(self, other):
        self._discriminated = other._discriminated
        rhs = getattr(other, self._discriminated.name)
        if codec_kind.is_composite(self._discriminated.type):
            lhs = getattr(self, self._discriminated.name)
            lhs.copy_from(rhs)
        else:
            setattr(self, self._discriminated.name, rhs)


def bytes_(**kwargs):
    size = kwargs.pop("size", 0)
    bound = kwargs.pop("bound", None)
    shift = kwargs.pop("shift", 0)
    if shift and (not bound or size):
        raise ProphyError("only shifting bound bytes implemented")
    if kwargs:
        raise ProphyError("unknown arguments to bytes field")

    class _bytes(bytes):
        _SIZE = size
        _DYNAMIC = not size
        _UNLIMITED = not size and not bound
        _DEFAULT = b"\x00" * size if size and not bound else ""
        _OPTIONAL = False
        _ALIGNMENT = 1
        _BOUND = bound
        _BOUND_SHIFT = shift
        _PARTIAL_ALIGNMENT = None
        _is_prophy_object = True

        @staticmethod
        def _check(value):
            if not isinstance(value, bytes):
                raise ProphyError("not a bytes")
            if size and len(value) > size:
                raise ProphyError("too long")
            if size and not bound:
                return value.ljust(size, b'\x00')
            return value

        @staticmethod
        def _encode(value):
            return value.ljust(size, b'\x00')

        @staticmethod
        def _decode(data, pos, len_hint):
            if (len(data) - pos) < size:
                raise ProphyError("too few bytes to decode string")
            if size and not bound:
                return data[pos:(pos + size)], size
            elif size and bound:
                return data[pos:(pos + len_hint)], size
            elif bound:
                if (len(data) - pos) < len_hint:
                    raise ProphyError("too few bytes to decode string")
                return data[pos:(pos + len_hint)], len_hint
            else:  # greedy
                return data[pos:], (len(data) - pos)

    return _bytes


class codec_kind(object):
    ARRAY = "ARRAY"
    ARRAY_SIZER = "ARRAY_SIZER"
    BYTES = "BYTES"
    COMPOSITE = "COMPOSITE"
    OPTIONAL = "OPTIONAL"
    SCALAR = "SCALAR"

    @classmethod
    def is_optional(cls, type_):
        return bool(type_._OPTIONAL)

    @classmethod
    def is_array_sizer(cls, type_):
        return type_._BOUND and issubclass(type_, (int, long))

    @classmethod
    def is_array(cls, type_):
        return issubclass(type_, base_array)

    @classmethod
    def is_struct(cls, type_):
        return issubclass(type_, struct)

    @classmethod
    def is_union(cls, type_):
        return issubclass(type_, union)

    @classmethod
    def is_composite(cls, type_):
        return issubclass(type_, (struct, union))

    @classmethod
    def is_bytes(cls, type_):
        return issubclass(type_, bytes)

    @classmethod
    def is_enum(cls, type_):
        return issubclass(type_, enum)

    @classmethod
    def classify(cls, type_):
        mapping = [
            (cls.is_optional, cls.OPTIONAL),
            (cls.is_array_sizer, cls.ARRAY_SIZER),
            (cls.is_array, cls.ARRAY),
            (cls.is_composite, cls.COMPOSITE),
            (cls.is_bytes, cls.BYTES),
        ]
        for method, kind in mapping:
            if method(type_):
                return kind
        return cls.SCALAR
