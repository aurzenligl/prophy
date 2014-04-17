import struct

def int_decorator(size, id, min, max):
    def decorator(cls):
        @staticmethod
        def check(value):
            if not isinstance(value, (int, long)):
                raise Exception("not an int")
            if not min <= value <= max:
                raise Exception("out of bounds")
            return value

        @staticmethod
        def encode(value, endianess):
            return struct.pack(endianess + id, value)

        @staticmethod
        def decode(data, endianess):
            if len(data) < size:
                raise Exception("too few bytes to decode integer")
            value, = struct.unpack(endianess + id, data[:size])
            return value, size

        cls._check = check
        cls._encode = encode
        cls._decode = decode
        cls._tags = ["scalar", "unsigned_integer"]
        cls._DEFAULT = 0
        cls._SIZE = size
        cls._ALIGNMENT = size
        cls._DYNAMIC = False
        cls._UNLIMITED = False
        cls._OPTIONAL = False
        return cls
    return decorator

def float_decorator(size, id):
    def decorator(cls):
        @staticmethod
        def check(value):
            if not isinstance(value, (float, int, long)):
                raise Exception("not a float")
            return value

        @staticmethod
        def encode(value, endianess):
            return struct.pack(endianess + id, value)

        @staticmethod
        def decode(data, endianess):
            if len(data) < size:
                raise Exception("too few bytes to decode integer")
            value, = struct.unpack(endianess + id, data[:size])
            return value, size

        cls._check = check
        cls._encode = encode
        cls._decode = decode
        cls._tags = ["scalar"]
        cls._DEFAULT = 0.0
        cls._SIZE = size
        cls._ALIGNMENT = size
        cls._DYNAMIC = False
        cls._UNLIMITED = False
        cls._OPTIONAL = False
        return cls
    return decorator

@int_decorator(size = 1, id = 'b', min = -(1 << 7), max = (1 << 7) - 1)
class i8(int):
    pass

@int_decorator(size = 2, id = 'h', min = -(1 << 15), max = (1 << 15) - 1)
class i16(int):
    pass

@int_decorator(size = 4, id = 'i', min = -(1 << 31), max = (1 << 31) - 1)
class i32(int):
    pass

@int_decorator(size = 8, id = 'q', min = -(1 << 63), max = (1 << 63) - 1)
class i64(int):
    pass

@int_decorator(size = 1, id = 'B', min = 0, max = (1 << 8) - 1)
class u8(int):
    pass

@int_decorator(size = 2, id = 'H', min = 0, max = (1 << 16) - 1)
class u16(int):
    pass

@int_decorator(size = 4, id = 'I', min = 0, max = (1 << 32) - 1)
class u32(int):
    pass

@int_decorator(size = 8, id = 'Q', min = 0, max = (1 << 64) - 1)
class u64(int):
    pass

@float_decorator(size = 4, id = 'f')
class r32(int):
    pass

@float_decorator(size = 8, id = 'd')
class r64(int):
    pass

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
        _OPTIONAL = False
        _ALIGNMENT = 1

        @staticmethod
        def _check(value):
            if not isinstance(value, str):
                raise Exception("not a str")
            if size and len(value) > size:
                raise Exception("too long")
            if "static" in tags:
                return value.ljust(size, '\x00')
            return value

        @staticmethod
        def _encode(value, endianess):
            return value.ljust(size, '\x00')

        @staticmethod
        def _decode(data, endianess, len_hint):
            if len(data) < size:
                raise Exception("too few bytes to decode string")
            if "static" in tags:
                return data[:size], size
            elif "limited" in tags:
                return data[:len_hint], size
            elif "bound" in tags:
                if len(data) < len_hint:
                    raise Exception("too few bytes to decode string")
                return data[:len_hint], len_hint
            else:  # greedy
                return data, len(data)

        if bound:
            _LENGTH_FIELD = bound
            _LENGTH_SHIFT = shift
    return _bytes
