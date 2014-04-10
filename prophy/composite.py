import scalar
from itertools import ifilter

def validate(descriptor):
    if any(type._UNLIMITED for _, type in descriptor[:-1]):
        raise Exception("unlimited field is not the last one")

def add_attributes(cls, descriptor):
    cls._SIZE = sum(type._SIZE for _, type in descriptor)
    cls._SIZE += sum(x._optional_type._SIZE for x in filter(lambda x: x._OPTIONAL, (type for _, type in descriptor)))
    cls._DYNAMIC = any(type._DYNAMIC for _, type in descriptor)
    cls._UNLIMITED = any(type._UNLIMITED for _, type in descriptor)
    cls._OPTIONAL = False

def add_properties(cls, descriptor):
    for field_name, field_type in descriptor:
        if "repeated" in field_type._tags:
            add_repeated(cls, field_name, field_type)
        elif "composite" in field_type._tags:
            add_composite(cls, field_name, field_type)
        else:
            add_scalar(cls, field_name, field_type)

def add_repeated(cls, field_name, field_type):
    def getter(self):
        field_value = self._fields.get(field_name)
        if field_value is None:
            field_value = field_type()
            field_value = self._fields.setdefault(field_name, field_value)
        return field_value
    def setter(self, new_value):
        raise Exception("assignment to array field not allowed")
    setattr(cls, field_name, property(getter, setter))
    if hasattr(field_type, "_LENGTH_FIELD"):
        bound_name = field_type._LENGTH_FIELD
        index, bound_type = ((index, field[1]) for index, field in enumerate(cls._descriptor) if field[0] == bound_name).next()
        if bound_type._OPTIONAL:
            raise Exception("array must not be bound to optional field")
        if "unsigned_integer" not in bound_type._tags:
            raise Exception("array must be bound to an unsigned integer")
        class bound_int(bound_type):
            _bound = field_name
            _LENGTH_SHIFT = field_type._LENGTH_SHIFT
        cls._descriptor[index] = (bound_name, bound_int)
        delattr(cls, bound_name)

def add_scalar(cls, field_name, field_type):
    def getter(self):
        if field_type._OPTIONAL and field_name not in self._fields:
            return None
        value = self._fields.get(field_name, field_type._DEFAULT)
        if "enum" in field_type._tags:
            value = field_type._int_to_name[value]
        return value
    def setter(self, new_value):
        if field_type._OPTIONAL and new_value is None:
            self._fields.pop(field_name, None)
        else:
            self._fields[field_name] = field_type._check(new_value)
    setattr(cls, field_name, property(getter, setter))
    if hasattr(field_type, "_LENGTH_FIELD"):
        bound_name = field_type._LENGTH_FIELD
        index, bound_type = ((index, field[1]) for index, field in enumerate(cls._descriptor) if field[0] == bound_name).next()
        if "unsigned_integer" not in bound_type._tags:
            raise Exception("array must be bound to an unsigned integer")
        class bound_int(bound_type):
            _bound = field_name
            _LENGTH_SHIFT = field_type._LENGTH_SHIFT
        cls._descriptor[index] = (bound_name, bound_int)
        delattr(cls, bound_name)

def add_composite(cls, field_name, field_type):
    def getter(self):
        if field_type._OPTIONAL and field_name not in self._fields:
            return None
        if field_name not in self._fields:
            value = field_type()
            self._fields[field_name] = value
            return value
        else:
            return self._fields.get(field_name)
    def setter(self, new_value):
        if field_type._OPTIONAL and new_value is True:
            self._fields[field_name] = field_type()
        elif field_type._OPTIONAL and new_value is None:
            self._fields.pop(field_name, None)
        else:
            raise Exception("assignment to composite field not allowed")
    setattr(cls, field_name, property(getter, setter))

def indent(lines, spaces):
    return "\n".join((spaces * " ") + i for i in lines.splitlines()) + "\n"

def field_to_string(name, type, value):
    if "repeated" in type._tags:
        return "".join(field_to_string(name, type._TYPE, elem) for elem in value)
    elif "composite" in type._tags:
        return "%s {\n%s}\n" % (name, indent(str(value), spaces = 2))
    elif "string" in type._tags:
        return "%s: %s\n" % (name, repr(value))
    else:
        return "%s: %s\n" % (name, value)

def encode_field(type, value, endianess):
    if "repeated" in type._tags:
        return "".join(encode_field(type._TYPE, elem, endianess) for elem in value).ljust(type._SIZE, "\x00")
    elif "composite" in type._tags:
        return value.encode(endianess)
    elif "string" in type._tags:
        return value.ljust(type._SIZE, '\x00')
    elif "enum" in type._tags:
        numeric_value = value if isinstance(value, int) else type._name_to_int[value]
        return type._encode(numeric_value, endianess)
    else:
        return type._encode(value, endianess)

def decode_field(parent, name, type, data, endianess):
    if "repeated" in type._tags:
        if "composite" in type._TYPE._tags:
            if type._SIZE > len(data):
                raise Exception("too few bytes to decode array")
            value = getattr(parent, name)
            decoded = 0
            if "greedy" in type._tags:
                del value[:]
                while decoded < len(data):
                    decoded += value.add().decode(data[decoded:], endianess, terminal = False)
            else:
                for elem in value:
                    decoded += elem.decode(data[decoded:], endianess, terminal = False)
            return max(decoded, type._SIZE)
        else:
            if type._SIZE > len(data):
                raise Exception("too few bytes to decode array")
            value = getattr(parent, name)
            decoded = 0
            if "greedy" in type._tags:
                del value[:]
                while decoded < len(data):
                    elem, elem_size = value._TYPE._decode(data[decoded:], endianess)
                    value.append(elem)
                    decoded += elem_size
            else:
                for i in xrange(len(value)):
                    elem, elem_size = value._TYPE._decode(data[decoded:], endianess)
                    value[i] = elem
                    decoded += elem_size
            return max(decoded, type._SIZE)
    elif "composite" in type._tags:
        return getattr(parent, name).decode(data, endianess, terminal = False)
    elif "string" in type._tags:
        current_size = len(getattr(parent, name))
        if len(data) < type._SIZE:
            raise Exception("too few bytes to decode string")
        if "static" in type._tags:
            setattr(parent, name, data[:type._SIZE])
            return type._SIZE
        elif "limited" in type._tags:
            setattr(parent, name, data[:current_size])
            return type._SIZE
        elif "bound" in type._tags:
            if len(data) < current_size:
                raise Exception("too few bytes to decode string")
            setattr(parent, name, data[:current_size])
            return current_size
        else:  # greedy
            setattr(parent, name, data)
            return len(data)
    else:
        value, size = type._decode(data, endianess)
        if hasattr(type, "_bound"):
            ARRAY_GUARD = 65536
            if value > ARRAY_GUARD:
                raise Exception("decoded array length over %s" % ARRAY_GUARD)
            if value < type._LENGTH_SHIFT:
                raise Exception("decoded array length smaller than shift")
            value -= type._LENGTH_SHIFT
            array_value = getattr(parent, type._bound)
            if isinstance(array_value, str):
                setattr(parent, type._bound, "\x00" * value)
            else:
                array_element_type = array_value._TYPE
                if "composite" in array_element_type._tags:
                    del array_value[:]
                    array_value.extend([array_element_type() for _ in range(value)])
                else:
                    array_value[:] = [array_element_type._DEFAULT] * value
        else:
            setattr(parent, name, value)
        return size

class struct(object):
    __slots__ = []
    _tags = ["composite"]

    def __init__(self):
        self._fields = {}

    def __str__(self):
        out = ""
        for name, type in self._descriptor:
            value = getattr(self, name, None)
            if value is not None:
                out += field_to_string(name, type, value)
        return out

    def encode(self, endianess):
        out = ""
        for name, type in self._descriptor:
            value = getattr(self, name, None)
            if type._OPTIONAL and value is None:
                out += type._optional_type._encode(False, endianess)
                out += "\x00" * type._SIZE
            elif type._OPTIONAL:
                out += type._optional_type._encode(True, endianess)
                out += encode_field(type, value, endianess)
            elif hasattr(type, "_bound"):
                array_value = getattr(self, type._bound)
                out += type._encode(len(array_value) + type._LENGTH_SHIFT, endianess)
            else:
                out += encode_field(type, value, endianess)
        return out

    def decode(self, data, endianess, terminal = True):
        bytes_read = 0
        for name, type in self._descriptor:
            if type._OPTIONAL:
                value, size = type._optional_type._decode(data, endianess)
                data = data[size:]
                bytes_read += size
                if value:
                    setattr(self, name, True)
                else:
                    setattr(self, name, None)
                    data = data[type._SIZE:]
                    bytes_read += type._SIZE
                    continue
            size = decode_field(self, name, type, data, endianess)
            data = data[size:]
            bytes_read += size
        if terminal and data:
            raise Exception("not all bytes read")
        return bytes_read

    def copy_from(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Parameter to copy_from must be instance of same class.")
        if other is self:
            return

        fields = self._fields

        for name, value in other._fields.iteritems():
            cls = (cls for dsc_name, cls in self._descriptor if dsc_name == name).next()
            if "repeated" in cls._tags:
                field_value = getattr(self, name)
                if "composite" in cls._TYPE._tags:
                    if len(field_value) != len(value):
                        del field_value[:]
                        field_value.extend(value[:])
                    else:
                        for elem, other_elem in zip(field_value, value):
                            elem.copy_from(other_elem)
                else:
                    field_value[:] = value[:]
            elif "composite" in cls._tags:
                field_value = getattr(self, name)
                field_value.copy_from(value)
            else:
                fields[name] = value

class struct_generator(type):
    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = ["_fields"]
        return super(struct_generator, cls).__new__(cls, name, bases, attrs)
    def __init__(cls, name, bases, attrs):
        descriptor = cls._descriptor
        validate(descriptor)
        add_attributes(cls, descriptor)
        add_properties(cls, descriptor)
        super(struct_generator, cls).__init__(name, bases, attrs)

def validate_union(descriptor):
    if any(type._DYNAMIC for _, type, _ in descriptor):
        raise Exception("dynamic types not allowed in union")
    if any(hasattr(type, "_LENGTH_FIELD") and type._LENGTH_FIELD for _, type, _ in descriptor):
        raise Exception("bound array/bytes not allowed in union")
    if any("repeated" in type._tags for _, type, _ in descriptor):
        raise Exception("static array not implemented in union")
    if any(type._OPTIONAL for _, type, _ in descriptor):
        raise Exception("union with optional field disallowed")

def add_union_attributes(cls, descriptor):
    cls._discriminator_type = scalar.u32
    cls._SIZE = cls._discriminator_type._SIZE + max(type._SIZE for _, type, _ in descriptor)
    cls._DYNAMIC = False
    cls._UNLIMITED = False
    cls._OPTIONAL = False

def add_union_properties(cls, descriptor):
    add_union_discriminator(cls)
    for name, type, disc in descriptor:
        if "composite" in type._tags:
            add_union_composite(cls, name, type, disc)
        else:
            add_union_scalar(cls, name, type, disc)

def add_union_discriminator(cls):
    def getter(self):
        return self._discriminator
    def setter(self, new_value):
        field = next(ifilter(lambda x: new_value in (x[0], x[2]), self._descriptor), None)
        if field:
            name, type, disc = field
            if disc != self._discriminator:
                self._discriminator = disc
                self._fields = {}
        else:
            raise Exception("unknown discriminator")
    setattr(cls, "discriminator", property(getter, setter))

def add_union_scalar(cls, name, type, disc):
    def getter(self):
        if self._discriminator is not disc:
            raise Exception("currently field %s is discriminated" % self._discriminator)
        value = self._fields.get(name, type._DEFAULT)
        if "enum" in type._tags:
            value = type._int_to_name[value]
        return value
    def setter(self, new_value):
        if self._discriminator is not disc:
            raise Exception("currently field %s is discriminated" % self._discriminator)
        new_value = type._check(new_value)
        self._fields[name] = new_value
    setattr(cls, name, property(getter, setter))

def add_union_composite(cls, name, type, disc):
    def getter(self):
        if self._discriminator is not disc:
            raise Exception("currently field %s is discriminated" % self._discriminator)
        value = self._fields.get(name)
        if value is None:
            value = type()
            value = self._fields.setdefault(name, value)
        return value
    def setter(self, new_value):
        raise Exception("assignment to composite field not allowed")
    setattr(cls, name, property(getter, setter))

class union(object):
    __slots__ = []
    _tags = ["composite", "union"]

    def __init__(self):
        self._fields = {}
        self._discriminator = self._descriptor[0][2]

    def __str__(self):
        name, type, _ = next(ifilter(lambda x: x[2] == self._discriminator, self._descriptor))
        value = getattr(self, name)
        return field_to_string(name, type, value)

    def encode(self, endianess):
        name, type, _ = next(ifilter(lambda x: x[2] == self._discriminator, self._descriptor))
        value = getattr(self, name)
        bytes = self._discriminator_type._encode(self._discriminator, endianess) + encode_field(type, value, endianess)
        return bytes + "\x00" * (self._SIZE - len(bytes))

    def decode(self, data, endianess, terminal = True):
        disc, bytes_read = self._discriminator_type._decode(data, endianess)
        field = next(ifilter(lambda x: x[2] == disc, self._descriptor), None)
        if not field:
            raise Exception("unknown discriminator")
        self._discriminator = disc
        name, type, _ = field
        bytes_read += decode_field(self, name, type, data[bytes_read:], endianess)
        if len(data) < self._SIZE:
            raise Exception("not enough bytes")
        if terminal and len(data) > self._SIZE:
            raise Exception("not all bytes read")
        return self._SIZE

    def copy_from(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Parameter to copy_from must be instance of same class.")
        if other is self:
            return

        disc = other._discriminator
        self._discriminator = disc
        self._fields = {}
        name, type, _ = next(ifilter(lambda x: x[2] == disc, self._descriptor))
        value = getattr(self, name)
        if "composite" in type._tags:
            getattr(self, name).copy_from(getattr(other, name))
        else:
            setattr(self, name, getattr(other, name))

class union_generator(type):
    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = ["_fields", "_discriminator"]
        return super(union_generator, cls).__new__(cls, name, bases, attrs)
    def __init__(cls, name, bases, attrs):
        descriptor = cls._descriptor
        validate_union(descriptor)
        add_union_attributes(cls, descriptor)
        add_union_properties(cls, descriptor)
        super(union_generator, cls).__init__(name, bases, attrs)
