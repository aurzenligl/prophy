import struct

def int_generator(name, bases, attrs):
    min = attrs["_MIN"]
    max = attrs["_MAX"]
    id = attrs["_TYPE"]
    size = attrs["_SIZE"]

    def check(value):
        if not isinstance(value, (int, long)):
            raise Exception("not an int")
        if not min <= value <= max:
            raise Exception("out of bounds")
        return value

    def encode(value, endianess):
        return struct.pack(endianess + id, value)

    def decode(data, endianess):
        if len(data) < size:
            raise Exception("too few bytes to decode integer")
        value, = struct.unpack(endianess + id, data[:size])
        return value, size

    attrs["_check"] = staticmethod(check)
    attrs["_encode"] = staticmethod(encode)
    attrs["_decode"] = staticmethod(decode)
    return type(name, bases, attrs)

def float_generator(name, bases, attrs):
    id = attrs["_TYPE"]
    size = attrs["_SIZE"]

    def check(value):
        if not isinstance(value, (float, int, long)):
            raise Exception("not a float")
        return value

    def encode(value, endianess):
        return struct.pack(endianess + id, value)

    def decode(data, endianess):
        if len(data) < size:
            raise Exception("too few bytes to decode integer")
        value, = struct.unpack(endianess + id, data[:size])
        return value, size

    attrs["_check"] = staticmethod(check)
    attrs["_encode"] = staticmethod(encode)
    attrs["_decode"] = staticmethod(decode)
    return type(name, bases, attrs)

class int_base(object):
    _tags = ["scalar"]
    _DEFAULT = 0
    _DYNAMIC = False
    _UNLIMITED = False

class float_base(int_base):
    _DEFAULT = 0.0

class i8(int_base):
    _tags = int_base._tags + ["unsigned_integer"]
    __metaclass__ = int_generator
    _MIN = -(1 << 7)
    _MAX = (1 << 7) - 1
    _TYPE = "b"
    _SIZE = 1

class i16(int_base):
    _tags = int_base._tags + ["unsigned_integer"]
    __metaclass__ = int_generator
    _MIN = -(1 << 15)
    _MAX = (1 << 15) - 1
    _TYPE = "h"
    _SIZE = 2

class i32(int_base):
    _tags = int_base._tags + ["unsigned_integer"]
    __metaclass__ = int_generator
    _MIN = -(1 << 31)
    _MAX = (1 << 31) - 1
    _TYPE = "i"
    _SIZE = 4

class i64(int_base):
    _tags = int_base._tags + ["unsigned_integer"]
    __metaclass__ = int_generator
    _MIN = -(1 << 63)
    _MAX = (1 << 63) - 1
    _TYPE = "q"
    _SIZE = 8

class u8(int_base):
    _tags = int_base._tags + ["unsigned_integer"]
    __metaclass__ = int_generator
    _MIN = 0
    _MAX = (1 << 8) - 1
    _TYPE = "B"
    _SIZE = 1

class u16(int_base):
    _tags = int_base._tags + ["unsigned_integer"]
    __metaclass__ = int_generator
    _MIN = 0
    _MAX = (1 << 16) - 1
    _TYPE = "H"
    _SIZE = 2

class u32(int_base):
    _tags = int_base._tags + ["unsigned_integer"]
    __metaclass__ = int_generator
    _MIN = 0
    _MAX = (1 << 32) - 1
    _TYPE = "I"
    _SIZE = 4

class u64(int_base):
    _tags = int_base._tags + ["unsigned_integer"]
    __metaclass__ = int_generator
    _MIN = 0
    _MAX = (1 << 64) - 1
    _TYPE = "Q"
    _SIZE = 8

class r32(float_base):
    _tags = float_base._tags + ["signed_float"]
    __metaclass__ = float_generator
    _TYPE = "f"
    _SIZE = 4

class r64(float_base):
    _tags = float_base._tags + ["signed_float"]
    __metaclass__ = float_generator
    _TYPE = "d"
    _SIZE = 8

def enum_generator(name, bases, attrs):

    def check(value):
        if isinstance(value, str):
            value = name_to_int.get(value)
            if value is None:
                raise Exception("unknown enumerator name")
            return value
        elif isinstance(value, (int, long)):
            if not value in int_to_name:
                raise Exception("unknown enumerator value")
            return value
        else:
            raise Exception("neither string nor int")

    enumerators = attrs["_enumerators"]
    name_to_int = {name:value for name, value in enumerators}
    int_to_name = {value:name for name, value in enumerators}
    if len(name_to_int) < len(enumerators):
        raise Exception("names overlap")
    if len(int_to_name) < len(enumerators):
        raise Exception("values overlap")
    map(bases[0]._check, (value for _, value in enumerators))
    attrs["_DEFAULT"] = enumerators[0][1]
    attrs["_name_to_int"] = name_to_int
    attrs["_int_to_name"] = int_to_name
    attrs["_check"] = staticmethod(check)

    return type(name, bases, attrs)

class enum(u32):
    _tags = u32._tags + ["enum"]

class enum8(u8):
    _tags = u8._tags + ["enum"]

def bytes(**kwargs):
    size = kwargs.pop("size", 0)
    bound = kwargs.pop("bound", "")
    shift = kwargs.pop("shift", 0)
    if shift and (not bound or size):
        raise Exception("only shifting bound bytes implemented")
    if kwargs:
        raise Exception("unknown arguments to bytes field")

    tags = {"scalar", "string"}
    default = ""
    if size and bound:
        tags.add("limited")
    elif size and not bound:
        tags.add("static")
        default = "\x00" * size
    elif not size and not bound:
        tags.add("greedy")
    elif not size and bound:
        tags.add("bound")

    class _bytes(object):
        _tags = tags
        _SIZE = size
        _DYNAMIC = not size
        _UNLIMITED = not size and not bound
        _DEFAULT = default

        @staticmethod
        def _check(value):
            if not isinstance(value, str):
                raise Exception("not a str")
            if size and len(value) > size:
                raise Exception("too long")
            if "static" in tags:
                return value.ljust(size, '\x00')
            return value

        if bound:
            _LENGTH_FIELD = bound
            _LENGTH_SHIFT = shift
    return _bytes
