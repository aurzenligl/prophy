from struct import pack, unpack

class int_checker(object):
    def __init__(self, min_value, max_value):
        self.min = min_value
        self.max = max_value
    def check(self, proposed_value):
        if not isinstance(proposed_value, (int, long)):
            raise Exception("not an int")
        if not self.min <= proposed_value <= self.max:
            raise Exception("out of bounds")
        return proposed_value

class float_checker(object):
    def check(self, proposed_value):
        if not isinstance(proposed_value, (float, int, long)):
            raise Exception("not a float")
        return proposed_value

class encoder(object):
    def __init__(self, struct_type):
        self.type = struct_type
    def encode(self, value, endianess):
        return pack(endianess + self.type, value)

class decoder(object):
    def __init__(self, struct_type, size):
        self.type = struct_type
        self.size = size
    def decode(self, data, endianess):
        size = self.size
        if len(data) < size:
            raise Exception("too few bytes to decode integer")
        int_data = data[:size]
        value, = unpack(endianess + self.type, int_data)
        return value, size

def int_generator(name, bases, attrs):
    attrs["_checker"] = int_checker(attrs["_MIN"], attrs["_MAX"])
    attrs["_encoder"] = encoder(attrs["_TYPE"])
    attrs["_decoder"] = decoder(attrs["_TYPE"], attrs["_SIZE"])
    return type(name, bases, attrs)

def float_generator(name, bases, attrs):
    attrs["_checker"] = float_checker()
    attrs["_encoder"] = encoder(attrs["_TYPE"])
    attrs["_decoder"] = decoder(attrs["_TYPE"], attrs["_SIZE"])
    return type(name, bases, attrs)

class int_base(object):
    _tags = ["scalar"]
    _DEFAULT = 0

class float_base(object):
    _tags = ["scalar"]
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
    _tags = int_base._tags + ["signed_float"]
    __metaclass__ = float_generator
    _TYPE = "f"
    _SIZE = 4

class r64(float_base):
    _tags = int_base._tags + ["signed_float"]
    __metaclass__ = float_generator
    _TYPE = "d"
    _SIZE = 8

class enum_checker(object):
    def __init__(self, name_to_int, int_to_name):
        self.name_to_int = name_to_int
        self.int_to_name = int_to_name
    def check(self, proposed_value):
        if isinstance(proposed_value, str):
            value = self.name_to_int.get(proposed_value)
            if value is None:
                raise Exception("unknown enumerator name")
            return value
        elif isinstance(proposed_value, (int, long)):
            if not proposed_value in self.int_to_name:
                raise Exception("unknown enumerator value")
            return proposed_value
        else:
            raise Exception("neither string nor int")

def enum_generator(name, bases, attrs):
    enumerators = attrs["_enumerators"]
    attrs["_DEFAULT"] = enumerators[0][1]
    name_to_int = {}
    int_to_name = {}
    if len(set([ename for ename, _ in enumerators])) != len(enumerators):
        raise Exception("names overlap")
    if len(set([value for _, value in enumerators])) != len(enumerators):
        raise Exception("values overlap")
    for _, value in enumerators:
        bases[0]._base._checker.check(value)
    for ename, value in enumerators:
        name_to_int[ename] = value
        int_to_name[value] = ename
    attrs["_name_to_int"] = name_to_int
    attrs["_int_to_name"] = int_to_name
    attrs["_checker"] = enum_checker(name_to_int, int_to_name)
    return type(name, bases, attrs)

def base_enum_generator(name, bases, attrs):
    base = attrs["_base"]
    attrs["_tags"] = base._tags + ["enum"]
    bases = (base,)
    return type(name, bases, attrs)

class enum():
    __metaclass__ = base_enum_generator
    _base = u32

class enum8():
    __metaclass__ = base_enum_generator
    _base = u8

class bytes_base(object):
    _tags = ["scalar", "string"]

def bytes(**kwargs):
    if "shift" in kwargs and (not "bound" in kwargs or "size" in kwargs):
        raise Exception("only shifting bound bytes implemented")
    size = kwargs.pop("size", 0)
    bound = kwargs.pop("bound", "")
    shift = kwargs.pop("shift", 0)
    if kwargs:
        raise Exception("unknown arguments to bytes field")
    tags = []
    default = ""
    if size and bound:
        tags += ["limited"]
    elif size and not bound:
        tags += ["static"]
        default = "\x00" * size
    elif not size and not bound:
        tags += ["greedy"]
    elif not size and bound:
        tags += ["bound"]

    class checker(object):
        def check(self, proposed_value):
            if not isinstance(proposed_value, str):
                raise Exception("not a str")
            if size and len(proposed_value) > size:
                raise Exception("too long")
            if "static" in tags:
                return proposed_value.ljust(size, '\x00')
            return proposed_value

    class _bytes(bytes_base):
        _tags = bytes_base._tags + tags
        _SIZE = size
        _DEFAULT = default
        _checker = checker()
        if bound:
            _LENGTH_FIELD = bound
            _LENGTH_SHIFT = shift
    return _bytes
