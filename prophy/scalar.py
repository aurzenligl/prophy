import struct
from .exception import ProphyError
from .six import long

def numeric_decorator(cls, size, id):
    @staticmethod
    def encode(value, endianness):
        return struct.pack(endianness + id, value)

    @staticmethod
    def decode(data, pos, endianness):
        if (len(data) - pos) < size:
            raise ProphyError("too few bytes to decode integer")
        value, = struct.unpack(endianness + id, data[pos : pos + size])
        return value, size

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

def int_decorator(size, id, min, max):
    def decorator(cls):
        cls = numeric_decorator(cls, size, id)

        @staticmethod
        def check(value):
            if not isinstance(value, (int, long)):
                raise ProphyError("not an int")
            if not min <= value <= max:
                raise ProphyError("out of bounds")
            return value

        cls._check = check

        cls._DEFAULT = 0

        return cls
    return decorator

def float_decorator(size, id):
    def decorator(cls):
        cls = numeric_decorator(cls, size, id)

        @staticmethod
        def check(value):
            if not isinstance(value, (float, int, long)):
                raise ProphyError("not a float")
            return value

        cls._check = check

        cls._DEFAULT = 0.0

        return cls
    return decorator

@int_decorator(size = 1, id = 'b', min = -(1 << 7), max = (1 << 7) - 1)
class i8(long):
    __slots__ = []

@int_decorator(size = 2, id = 'h', min = -(1 << 15), max = (1 << 15) - 1)
class i16(long):
    __slots__ = []

@int_decorator(size = 4, id = 'i', min = -(1 << 31), max = (1 << 31) - 1)
class i32(long):
    __slots__ = []

@int_decorator(size = 8, id = 'q', min = -(1 << 63), max = (1 << 63) - 1)
class i64(long):
    __slots__ = []

@int_decorator(size = 1, id = 'B', min = 0, max = (1 << 8) - 1)
class u8(long):
    __slots__ = []

@int_decorator(size = 2, id = 'H', min = 0, max = (1 << 16) - 1)
class u16(long):
    __slots__ = []

@int_decorator(size = 4, id = 'I', min = 0, max = (1 << 32) - 1)
class u32(long):
    __slots__ = []

@int_decorator(size = 8, id = 'Q', min = 0, max = (1 << 64) - 1)
class u64(long):
    __slots__ = []

@float_decorator(size = 4, id = 'f')
class r32(float):
    __slots__ = []

@float_decorator(size = 8, id = 'd')
class r64(float):
    __slots__ = []

def add_enum_attributes(cls, enumerators):

    @staticmethod
    def check(value):
        if isinstance(value, str):
            value = name_to_int.get(value)
            if value is None:
                raise ProphyError("unknown enumerator name")
            return cls(value)
        elif isinstance(value, (int, long)):
            if not value in int_to_name:
                raise ProphyError("unknown enumerator value")
            return cls(value)
        else:
            raise ProphyError("neither string nor int")

    name_to_int = {name:value for name, value in enumerators}
    int_to_name = {value:name for name, value in enumerators}
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
                return data[pos:pos+size], size
            elif size and bound:
                return data[pos:pos+len_hint], size
            elif bound:
                if (len(data) - pos) < len_hint:
                    raise ProphyError("too few bytes to decode string")
                return data[pos:pos+len_hint], len_hint
            else:  # greedy
                return data[pos:], (len(data) - pos)

    return _bytes
