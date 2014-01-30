def check_greedy_field(descriptor, greedy_found = False):
    for _, field_type in descriptor:
        if "composite" in field_type._tags:
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
    if "composite" in field_type._TYPE._tags:
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
    
class struct_generator(type):
    def __new__(cls, name, bases, attrs):
        attrs["__slots__"] = ["_fields"]
        return super(struct_generator, cls).__new__(cls, name, bases, attrs)
    def __init__(cls, name, bases, attrs):
        descriptor = attrs["_descriptor"]
        add_properties(cls, descriptor)
        super(struct_generator, cls).__init__(name, bases, attrs)

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
        if not "composite" in field_type._TYPE._tags and field_type._LIMIT:
            remaining = field_type._LIMIT - len(field_value)
            out += remaining * encode_field(field_type._TYPE, field_type._TYPE._DEFAULT, endianess)
    elif "composite" in field_type._tags:
        out += field_value.encode(endianess)
    elif "string" in field_type._tags:
        out += field_value
        if field_type._LIMIT:
            out += "\x00" * (field_type._LIMIT - len(field_value))
    elif "enum" in field_type._tags:
        numeric_value = field_type._name_to_int[field_value]
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
        field_value = getattr(field_parent, field_name)
        size = len(field_value)
        if "greedy" in field_type._tags:
            size = len(data)
        else:
            if len(data) < size:
                raise Exception("too few bytes to decode string")
        setattr(field_parent, field_name, data[:size])
        if field_type._LIMIT:
            limit = field_type._LIMIT
            if len(data) < limit:
                raise Exception("too few bytes to decode limited string")
            size = limit
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
        