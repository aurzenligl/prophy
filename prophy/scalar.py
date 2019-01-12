import struct

from .exception import ProphyError
from .six import long


class prophy_data_object(object):
    _is_prophy_object = True
    __slots__ = []


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

    cls._is_prophy_object = True
    cls._encode = encode
    cls._decode = decode

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
                raise ProphyError("value: {} out of {}B integer's bounds: [{}, {}]".format(value, size, min_, max_))
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
class i8(long):
    __slots__ = []


@int_decorator(size=2, id_='h', min_=-(1 << 15), max_=(1 << 15) - 1)
class i16(long):
    __slots__ = []


@int_decorator(size=4, id_='i', min_=-(1 << 31), max_=(1 << 31) - 1)
class i32(long):
    __slots__ = []


@int_decorator(size=8, id_='q', min_=-(1 << 63), max_=(1 << 63) - 1)
class i64(long):
    __slots__ = []


@int_decorator(size=1, id_='B', min_=0, max_=(1 << 8) - 1)
class u8(long):
    __slots__ = []


@int_decorator(size=2, id_='H', min_=0, max_=(1 << 16) - 1)
class u16(long):
    __slots__ = []


@int_decorator(size=4, id_='I', min_=0, max_=(1 << 32) - 1)
class u32(long):
    __slots__ = []


@int_decorator(size=8, id_='Q', min_=0, max_=(1 << 64) - 1)
class u64(long):
    __slots__ = []


@float_decorator(size=4, id_='f')
class r32(float):
    __slots__ = []


@float_decorator(size=8, id_='d')
class r64(float):
    __slots__ = []


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
