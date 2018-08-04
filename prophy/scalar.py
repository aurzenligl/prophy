import struct

from .base import prophy_data_object
from .exception import ProphyError
from .six import long


@classmethod
def _bricks_walk(cls, cursor):
    yield cls, None


def numeric_decorator(cls, size, id_):
    @staticmethod
    def encode(value, endianness):
        return struct.pack(endianness + id_, value)

    @staticmethod
    def decode(data, pos, endianness):
        if (len(data) - pos) < size:
            raise ProphyError("too few bytes to decode integer")
        value, = struct.unpack(endianness + id_, data[pos:(pos + size)])
        return value, size

    cls._encode = encode
    cls._decode = decode
    cls._bricks_walk = _bricks_walk

    cls._SIZE = size
    cls._ALIGNMENT = size
    cls._DYNAMIC = False
    cls._UNLIMITED = False
    cls._OPTIONAL = False
    cls._BOUND = None
    cls._PARTIAL_ALIGNMENT = None

    return cls


def int_decorator(size, id_, min_, max_):
    def decorator(cls):
        cls = numeric_decorator(cls, size, id_)

        @staticmethod
        def check(value):
            if not isinstance(value, (int, long)):
                raise ProphyError("not an int")
            if not min_ <= value <= max_:
                raise ProphyError("out of bounds")
            return value

        cls._check = check

        cls._DEFAULT = 0

        return cls
    return decorator


def float_decorator(size, id_):
    def decorator(cls):
        cls = numeric_decorator(cls, size, id_)

        @staticmethod
        def check(value):
            if not isinstance(value, (float, int, long)):
                raise ProphyError("not a float")
            return value

        cls._check = check

        cls._DEFAULT = 0.0

        return cls
    return decorator


@int_decorator(size=1, id_='b', min_=-(1 << 7), max_=(1 << 7) - 1)
class i8(long, prophy_data_object):
    __slots__ = []


@int_decorator(size=2, id_='h', min_=-(1 << 15), max_=(1 << 15) - 1)
class i16(long, prophy_data_object):
    __slots__ = []


@int_decorator(size=4, id_='i', min_=-(1 << 31), max_=(1 << 31) - 1)
class i32(long, prophy_data_object):
    __slots__ = []


@int_decorator(size=8, id_='q', min_=-(1 << 63), max_=(1 << 63) - 1)
class i64(long, prophy_data_object):
    __slots__ = []


@int_decorator(size=1, id_='B', min_=0, max_=(1 << 8) - 1)
class u8(long, prophy_data_object):
    __slots__ = []


@int_decorator(size=2, id_='H', min_=0, max_=(1 << 16) - 1)
class u16(long, prophy_data_object):
    __slots__ = []


@int_decorator(size=4, id_='I', min_=0, max_=(1 << 32) - 1)
class u32(long, prophy_data_object):
    __slots__ = []


@int_decorator(size=8, id_='Q', min_=0, max_=(1 << 64) - 1)
class u64(long, prophy_data_object):
    __slots__ = []


@float_decorator(size=4, id_='f')
class r32(float, prophy_data_object):
    __slots__ = []


@float_decorator(size=8, id_='d')
class r64(float, prophy_data_object):
    __slots__ = []


def add_enum_attributes(cls, enumerators):

    @classmethod
    def check(cls, value):
        if isinstance(value, str):
            value = name_to_int.get(value)
            if value is None:
                raise ProphyError("unknown enumerator name in {}".format(cls.__name__))
            return cls(value)
        elif isinstance(value, (int, long)):
            if value not in int_to_name:
                raise ProphyError("unknown enumerator {} value".format(cls.__name__))
            return cls(value)
        else:
            raise ProphyError("neither string nor int")

    name_to_int = {name: value for name, value in enumerators}
    int_to_name = {value: name for name, value in enumerators}
    if len(name_to_int) < len(enumerators):
        raise ProphyError("names overlap")
    list(map(cls._check, (value for _, value in enumerators)))
    cls._DEFAULT = cls(enumerators[0][1])
    cls._name_to_int = name_to_int
    cls._int_to_name = int_to_name
    cls._check = check


class enum_generator(type):
    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = []
        return super(enum_generator, cls).__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "_generated"):
            cls._generated = True
            add_enum_attributes(cls, cls._enumerators)
        super(enum_generator, cls).__init__(name, bases, attrs)


class enum(u32, prophy_data_object):
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

    class _bytes(bytes, prophy_data_object):
        _SIZE = size
        _DYNAMIC = not size
        _UNLIMITED = not size and not bound
        _DEFAULT = b"\x00" * size if size and not bound else ""
        _OPTIONAL = False
        _ALIGNMENT = 1
        _BOUND = bound
        _BOUND_SHIFT = shift
        _PARTIAL_ALIGNMENT = None
        _bricks_walk = _bricks_walk

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
