from .exception import ProphyError
from .scalar import u32, u8, scalar_bricks_walk, prophy_data_object
from .six import repr_bytes, long


class base_array(prophy_data_object):
    __slots__ = ['_values']

    def __init__(self):
        self._values = []

    def __getitem__(self, idx):
        return self._values[idx]

    def __getslice__(self, start, stop):
        return self._values[start:stop]

    def __len__(self):
        return len(self._values)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        raise TypeError('unhashable object')

    def __repr__(self):
        return repr(self._values)

    def sort(self, key_function=lambda x: x):
        self._values.sort(key=key_function)

    @classmethod
    def _bricks_walk(cls, cursor):

        if cls._max_len:
            indexes = range(cls._max_len)
        else:
            if not cls._UNLIMITED:

                size_info = "@%s" % cls._BOUND
                if cls._max_len:
                    size_info += " %s" % cls._max_len
            else:
                size_info = "..."

            indexes = [size_info]

        for index in indexes:
            for brick_type, brick_path in cls._TYPE._bricks_walk(cursor):
                path_ = "[%s]%s" % (index, brick_path or "")
                yield brick_type, path_


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


class _composite_base(prophy_data_object):
    __slots__ = []

    def copy_from(self, other):
        self.validate_copy_from(other)
        if other is self:
            return

        self._fields.clear()
        self._copy_implementation(other)

    @classmethod
    def validate_copy_from(cls, rhs):
        if not isinstance(rhs, cls):
            raise TypeError("Parameter to copy_from must be instance of same class.")

    def _copy_implementation(self, other):
        " To be overrided in derived class "

    @classmethod
    def get_descriptor(cls):
        """
            FIXME: I'm afraid it rapes YAGNI rule
        """
        return [item.descriptor_info for item in cls._descriptor]

    @classmethod
    def _bricks_walk(cls, cursor):
        def eval_path(leaf_path):
            return ".%s%s" % (item.name, leaf_path or "")

        for item in cls._descriptor:

            padding_size = cursor.distance_to_next(item.type._ALIGNMENT)
            if padding_size:
                yield make_padding(padding_size), eval_path(".:pre_padding")

            for sub_brick_type, sub_brick_path in item.type._bricks_walk(cursor):
                yield sub_brick_type, eval_path(sub_brick_path)

            if item.type._PARTIAL_ALIGNMENT:
                padding_size = cursor.distance_to_next(item.type._PARTIAL_ALIGNMENT)
                if padding_size:
                    yield make_padding(padding_size), eval_path(".:partial_padding")

        padding_size = cursor.distance_to_next(cls._ALIGNMENT)
        if padding_size:
            yield make_padding(padding_size), eval_path(".:final_padding")

    @classmethod
    def wire_pattern(cls):
        cursor = _cursor_class()
        for type_, path_ in cls._bricks_walk(cursor):
            type_size = getattr(type_, "_SIZE", "??")
            if type_size != "??":
                cursor.pos += type_size
            yield path_, type_.__name__, type_size


class _cursor_class(object):
    """
        A helper for breaking variables scope while passing the "self.pos" between _bricks_walk iterators call.
        TODO: It will be probably not needed.
    """

    def __init__(self):
        self.pos = 0

    def distance_to_next(self, alignment):
        remainer = self.pos % alignment
        return (alignment - remainer) % alignment


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


class struct(_composite_base):
    _default_padding_value = b'\x00'
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
        return cls._default_padding_value * cls._get_padding_size(offset, alignment)

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

    # def encode_prototype(self, endianness):
    #     data = b""
    #     cursor = "_cursor_class()"
    #     # item, parent, path_, name
    #     for item, parent, path_ in self._bricks_walk(cursor):
    #         value = getattr(parent, item.name, None)
    #         data += item.encode_fcn(self, item.type, value, endianness)
    #         cursor.pos = len(data)
    #     return data

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
        """
            FIXME: I'm afraid it rapes YAGNI rule
        """
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

    def _copy_implementation(self, other):
        self._discriminated = other._discriminated
        rhs = getattr(other, self._discriminated.name)
        if codec_kind.is_composite(self._discriminated.type):
            lhs = getattr(self, self._discriminated.name)
            lhs.copy_from(rhs)
        else:
            setattr(self, self._discriminated.name, rhs)


class enum(u32):
    __slots__ = []

    @property
    def name(self):
        return self._int_to_name[self]

    @property
    def number(self):
        return int(self)


class enum8(u8, enum):
    __slots__ = []


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
        _bricks_walk = scalar_bricks_walk
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


class kind(type):
    """
        FIXME: I hope nobody needs that. I'm about to remove that.
    """
    INT = ('INT', 0)
    ENUM = ('ENUM', 1)
    BYTES = ('BYTES', 2)
    ARRAY = ('ARRAY', 3)
    STRUCT = ('STRUCT', 4)
    UNION = ('UNION', 5)


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
