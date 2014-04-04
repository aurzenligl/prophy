import scalar
from itertools import ifilter

def check_greedy_field(descriptor, greedy_found = False):
    for _, field_type in descriptor:
        if "union" in field_type._tags:
            pass
        elif "composite" in field_type._tags:
            greedy_found = check_greedy_field(field_type._descriptor, greedy_found)
        else:
            if greedy_found:
                raise Exception("greedy field is not the last one")
            if "greedy" in field_type._tags:
                greedy_found = True
    return greedy_found

def add_properties(cls, descriptor):
    check_greedy_field(descriptor)
    for field_name, field_type in descriptor:
        if "repeated" in field_type._tags:
            add_repeated(cls, field_name, field_type)
        elif "composite" in field_type._tags:
            add_composite(cls, field_name, field_type)
        else:
            add_scalar(cls, field_name, field_type)

def add_repeated(cls, field_name, field_type):
    if "union" in field_type._TYPE._tags:
        pass
    elif "composite" in field_type._TYPE._tags:
        if check_greedy_field(field_type._TYPE._descriptor):
            raise Exception("array with composite with greedy field disallowed")
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
        if "unsigned_integer" not in bound_type._tags:
            raise Exception("array must be bound to an unsigned integer")
        class bound_int(bound_type):
            _bound = field_name
            _LENGTH_SHIFT = field_type._LENGTH_SHIFT
        cls._descriptor[index] = (bound_name, bound_int)
        delattr(cls, bound_name)

def add_scalar(cls, field_name, field_type):
    def getter(self):
        value = self._fields.get(field_name, field_type._DEFAULT)
        if "enum" in field_type._tags:
            value = field_type._int_to_name[value]
        return value
    def setter(self, new_value):
        new_value = field_type._checker.check(new_value)
        self._fields[field_name] = new_value
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
        field_value = self._fields.get(field_name)
        if field_value is None:
            field_value = field_type()
            field_value = self._fields.setdefault(field_name, field_value)
        return field_value
    def setter(self, new_value):
        raise Exception("assignment to composite field not allowed")
    setattr(cls, field_name, property(getter, setter))

def indent(lines, spaces):
    return "\n".join((spaces * " ") + i for i in lines.splitlines()) + "\n"

def field_to_string(field_name, field_type, field_value):
    out = ""
    if "repeated" in field_type._tags:
        for elem in field_value:
            out += field_to_string(field_name, field_type._TYPE, elem)
    elif "composite" in field_type._tags:
        out += "%s {\n" % field_name
        out += indent(str(field_value), spaces = 2)
        out += "}\n"
    elif "string" in field_type._tags:
        out += "%s: %s\n" % (field_name, repr(field_value))
    else:
        out += "%s: %s\n" % (field_name, field_value)
    return out

def encode_field(field_type, field_value, endianess):
    out = ""
    if "repeated" in field_type._tags:
        for elem in field_value:
            out += encode_field(field_type._TYPE, elem, endianess)
        if field_type._LIMIT:
            remaining = field_type._LIMIT - len(field_value)
            default = field_type._TYPE() if "composite" in field_type._TYPE._tags else field_type._TYPE._DEFAULT
            out += remaining * encode_field(field_type._TYPE, default, endianess)
    elif "composite" in field_type._tags:
        out += field_value.encode(endianess)
    elif "string" in field_type._tags:
        out += field_value
        if field_type._LIMIT:
            out += "\x00" * (field_type._LIMIT - len(field_value))
    elif "enum" in field_type._tags:
        numeric_value = field_value if isinstance(field_value, int) else field_type._name_to_int[field_value]
        out += field_type._encoder.encode(numeric_value, endianess)
    else:
        out += field_type._encoder.encode(field_value, endianess)
    return out

def decode_field(field_parent, field_name, field_type, data, endianess):
    if "repeated" in field_type._tags:
        if "composite" in field_type._TYPE._tags:
            composite_array = getattr(field_parent, field_name)
            size = 0
            if "greedy" in field_type._tags:
                del composite_array[:]
                while size < len(data):
                    composite_value = composite_array.add()
                    bytes_read = composite_value.decode(data[size:], endianess, terminal = False)
                    size += bytes_read
            else:
                for composite_value in composite_array:
                    bytes_read = composite_value.decode(data[size:], endianess, terminal = False)
                    size += bytes_read
            if field_type._LIMIT:
                limit = field_type._LIMIT * len(field_type._TYPE().encode(">"))
                if len(data) < limit:
                    raise Exception("too few bytes to decode limited array")
                size = limit
        else:
            scalar_array = getattr(field_parent, field_name)
            scalar_decoder = scalar_array._TYPE._decoder
            size = 0
            if "greedy" in field_type._tags:
                del scalar_array[:]
                while size < len(data):
                    value, bytes_read = scalar_decoder.decode(data[size:], endianess)
                    scalar_array.append(value)
                    size += bytes_read
            else:
                for i in range(len(scalar_array)):
                    value, bytes_read = scalar_decoder.decode(data[size:], endianess)
                    scalar_array[i] = value
                    size += bytes_read
            if field_type._LIMIT:
                limit = field_type._LIMIT * field_type._TYPE._SIZE
                if len(data) < limit:
                    raise Exception("too few bytes to decode limited array")
                size = limit
    elif "composite" in field_type._tags:
        field_value = getattr(field_parent, field_name)
        size = field_value.decode(data, endianess, terminal = False)
    elif "string" in field_type._tags:
        current_size = len(getattr(field_parent, field_name))
        if len(data) < field_type._SIZE:
            raise Exception("too few bytes to decode string")
        if "static" in field_type._tags:
            setattr(field_parent, field_name, data[:field_type._SIZE])
            return field_type._SIZE
        elif "limited" in field_type._tags:
            setattr(field_parent, field_name, data[:current_size])
            return field_type._SIZE
        elif "bound" in field_type._tags:
            if len(data) < current_size:
                raise Exception("too few bytes to decode string")
            setattr(field_parent, field_name, data[:current_size])
            return current_size
        else:  # greedy
            setattr(field_parent, field_name, data)
            return len(data)
    else:
        value, size = field_type._decoder.decode(data, endianess)
        if hasattr(field_type, "_bound"):
            ARRAY_GUARD = 65536
            if value > ARRAY_GUARD:
                raise Exception("decoded array length over %s" % ARRAY_GUARD)
            if value < field_type._LENGTH_SHIFT:
                raise Exception("decoded array length smaller than shift")
            value -= field_type._LENGTH_SHIFT
            array_value = getattr(field_parent, field_type._bound)
            if isinstance(array_value, str):
                setattr(field_parent, field_type._bound, "\x00" * value)
            else:
                array_element_type = array_value._TYPE
                if "composite" in array_element_type._tags:
                    del array_value[:]
                    new_elements = [array_element_type() for _ in range(value)]
                    array_value.extend(new_elements)
                else:
                    array_value[:] = [array_element_type._DEFAULT] * value
        else:
            setattr(field_parent, field_name, value)
    return size

class struct(object):
    __slots__ = []
    _tags = ["composite"]

    def __init__(self):
        self._fields = {}

    def __str__(self):
        out = ""
        for field_name, field_type in self._descriptor:
            if hasattr(field_type, "_bound"):
                continue
            field_value = getattr(self, field_name)
            out += field_to_string(field_name, field_type, field_value)
        return out

    def encode(self, endianess):
        out = ""
        for field_name, field_type in self._descriptor:
            if hasattr(field_type, "_bound"):
                array_value = getattr(self, field_type._bound)
                out += field_type._encoder.encode(len(array_value) + field_type._LENGTH_SHIFT, endianess)
            else:
                field_value = getattr(self, field_name)
                out += encode_field(field_type, field_value, endianess)
        return out

    def decode(self, data, endianess, terminal = True):
        bytes_read = 0
        for field_name, field_type in self._descriptor:
            size = decode_field(self, field_name, field_type, data, endianess)
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
        descriptor = attrs["_descriptor"]
        add_properties(cls, descriptor)
        super(struct_generator, cls).__init__(name, bases, attrs)

def validate_union_type(type, static_containers = True):
    if "union" in type._tags:
        map(validate_union_type, (type for _, type, _ in type._descriptor))
    elif "composite" in type._tags:
        map(validate_union_type, (type for _, type in type._descriptor))
    elif "repeated" in type._tags:
        if not hasattr(type, "_SIZE"):
            raise Exception("non-sized array not allowed inside union")
        if not static_containers:
            raise Exception("array not allowed as union member")
    elif "string" in type._tags:
        if not type._LIMIT:
            raise Exception("non-sized bytes not allowed inside union")
        if not static_containers:
            raise Exception("bytes not allowed as union member")

def add_union_properties(cls, descriptor):
    add_union_size(cls, descriptor)
    add_union_discriminator(cls)
    for name, type, disc in descriptor:
        if "composite" in type._tags:
            add_union_composite(cls, name, type, disc)
        else:
            add_union_scalar(cls, name, type, disc)

def add_union_size(cls, descriptor):
    def field_size(type):
        if "composite" in type._tags:
            return len(type().encode(">"))
        else:
            return type._SIZE

    cls._SIZE = scalar.u32._SIZE + max(field_size(type) for _, type, _ in descriptor)

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
        new_value = type._checker.check(new_value)
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
        bytes = scalar.u32._encoder.encode(self._discriminator, endianess) + encode_field(type, value, endianess)
        return bytes + "\x00" * (self._SIZE - len(bytes))

    def decode(self, data, endianess, terminal = True):
        disc, bytes_read = scalar.u32._decoder.decode(data, endianess)
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
        descriptor = attrs["_descriptor"]
        map(lambda x: validate_union_type(x, static_containers = False), (type for _, type, _ in descriptor))
        add_union_properties(cls, descriptor)
        super(union_generator, cls).__init__(name, bases, attrs)
