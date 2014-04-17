class base_array(object):
    __slots__ = ['_values']
    _tags = ["repeated"]

    def __init__(self):
        self._values = []

    def __getitem__(self, key):
        return self._values[key]

    def __len__(self):
        return len(self._values)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        raise TypeError('unhashable object')

    def __repr__(self):
        return repr(self._values)

    def sort(self, sort_function = cmp):
        self._values.sort(sort_function)

class fixed_scalar_array(base_array):

    __slots__ = []

    def __init__(self):
        super(fixed_scalar_array, self).__init__()
        self._values = [self._TYPE._DEFAULT] * self._max_len

    def __setitem__(self, key, value):
        value = self._TYPE._check(value)
        self._values[key] = value

    def __getslice__(self, start, stop):
        return self._values[start:stop]

    def __setslice__(self, start, stop, values):
        if len(self._values[start:stop]) is not len(values):
            raise Exception("setting slice with different length collection")
        new_values = []
        for value in values:
            value = self._TYPE._check(value)
            new_values.append(value)
        self._values[start:stop] = new_values

    def __eq__(self, other):
        if self is other:
            return True
        # Special case for the same type which should be common and fast.
        if isinstance(other, self.__class__):
            return other._values == self._values
        # We are presumably comparing against some other sequence type.
        return other == self._values

class bound_scalar_array(base_array):

    __slots__ = []

    def __init__(self):
        super(bound_scalar_array, self).__init__()

    def append(self, value):
        value = self._TYPE._check(value)
        if self._max_len and len(self) == self._max_len:
            raise Exception("exceeded array limit")
        self._values.append(value)

    def insert(self, key, value):
        value = self._TYPE._check(value)
        if self._max_len and len(self) == self._max_len:
            raise Exception("exceeded array limit")
        self._values.insert(key, value)

    def extend(self, elem_seq):
        if not elem_seq:
            return
        if self._max_len and len(self) + len(elem_seq) > self._max_len:
            raise Exception("exceeded array limit")
        new_values = []
        for elem in elem_seq:
            elem = self._TYPE._check(elem)
            new_values.append(elem)
        self._values.extend(new_values)

    def remove(self, elem):
        self._values.remove(elem)

    def __setitem__(self, key, value):
        value = self._TYPE._check(value)
        self._values[key] = value

    def __getslice__(self, start, stop):
        return self._values[start:stop]

    def __setslice__(self, start, stop, values):
        if self._max_len and len(self) + len(values) - len(self._values[start:stop]) > self._max_len:
            raise Exception("exceeded array limit")
        new_values = []
        for value in values:
            value = self._TYPE._check(value)
            new_values.append(value)
        self._values[start:stop] = new_values

    def __delitem__(self, key):
        del self._values[key]

    def __delslice__(self, start, stop):
        del self._values[start:stop]

    def __eq__(self, other):
        if self is other:
            return True
        # Special case for the same type which should be common and fast.
        if isinstance(other, self.__class__):
            return other._values == self._values
        # We are presumably comparing against some other sequence type.
        return other == self._values

class fixed_composite_array(base_array):

    __slots__ = []

    def __init__(self):
        super(fixed_composite_array, self).__init__()
        self._values = [self._TYPE() for _ in xrange(self._max_len)]

    def __getslice__(self, start, stop):
        return self._values[start:stop]

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, self.__class__):
            raise TypeError('Can only compare repeated composite fields against '
                            'other repeated composite fields.')
        return self._values == other._values

class bound_composite_array(base_array):

    __slots__ = []

    def __init__(self):
        super(bound_composite_array, self).__init__()

    """ TODO kl. implement **kwargs to fill structure with data at addition time already """
    def add(self):
        if self._max_len and len(self) == self._max_len:
            raise Exception("exceeded array limit")

        new_element = self._TYPE()
        self._values.append(new_element)
        return new_element

    def extend(self, elem_seq):
        if self._max_len and len(self) + len(elem_seq) > self._max_len:
            raise Exception("exceeded array limit")

        composite_cls = self._TYPE
        for message in elem_seq:
            new_element = composite_cls()
            new_element.copy_from(message)
            self._values.append(new_element)

    def __getslice__(self, start, stop):
        return self._values[start:stop]

    def __delitem__(self, key):
        del self._values[key]

    def __delslice__(self, start, stop):
        del self._values[start:stop]

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, self.__class__):
            raise TypeError('Can only compare repeated composite fields against '
                            'other repeated composite fields.')
        return self._values == other._values

def array(type, **kwargs):
    size = kwargs.pop("size", 0)
    bound = kwargs.pop("bound", None)
    shift = kwargs.pop("shift", 0)
    if kwargs:
        raise Exception("unknown arguments to array field")

    if "repeated" in type._tags:
        raise Exception("array of arrays not allowed")
    if "string" in type._tags:
        raise Exception("array of strings not allowed")
    if size and type._DYNAMIC:
        raise Exception("static/limited array of dynamic type not allowed")
    if shift and (not bound or size):
        raise Exception("only shifting bound array implemented")
    if type._UNLIMITED:
        raise Exception("array with unlimited field disallowed")
    if type._OPTIONAL:
        raise Exception("array of optional type not allowed")

    is_composite = "composite" in type._tags

    tags = []

    if size and bound:
        base = bound_composite_array if is_composite else bound_scalar_array
    elif size and not bound:
        actual_size = 0
        base = fixed_composite_array if is_composite else fixed_scalar_array
    elif not size and bound:
        base = bound_composite_array if is_composite else bound_scalar_array
    elif not size and not bound:
        tags += ["greedy"]
        base = bound_composite_array if is_composite else bound_scalar_array

    class _array(base):
        __slots__ = []
        _tags = base._tags + tags
        _max_len = size
        _TYPE = type
        _SIZE = size * type._SIZE
        _DYNAMIC = not size
        _UNLIMITED = not size and not bound
        _OPTIONAL = False
        _ALIGNMENT = type._ALIGNMENT
        _BOUND = bound
        _BOUND_SHIFT = shift

        def encode(self, endianness):
            if issubclass(self._TYPE, int):
                data = "".join(self._TYPE._encode(value, endianness) for value in self)
            else:
                data = "".join(value.encode(endianness) for value in self)
            return data.ljust(self._SIZE, "\x00")

        def decode(self, data, endianness, len_hint):
            if "composite" in self._TYPE._tags:
                if self._SIZE > len(data):
                    raise Exception("too few bytes to decode array")
                if len_hint is not None:
                    del self[:]
                    self.extend([self._TYPE() for _ in xrange(len_hint)])

                decoded = 0
                if "greedy" in self._tags:
                    del self[:]
                    while decoded < len(data):
                        decoded += self.add().decode(data[decoded:], endianness, terminal = False)
                else:
                    for elem in self:
                        decoded += elem.decode(data[decoded:], endianness, terminal = False)
                return max(decoded, self._SIZE)
            else:
                if self._SIZE > len(data):
                    raise Exception("too few bytes to decode array")
                if len_hint is not None:
                    self[:] = [self._TYPE._DEFAULT] * len_hint

                decoded = 0
                if "greedy" in self._tags:
                    del self[:]
                    while decoded < len(data):
                        elem, elem_size = self._TYPE._decode(data[decoded:], endianness)
                        self.append(elem)
                        decoded += elem_size
                else:
                    for i in xrange(len(self)):
                        elem, elem_size = self._TYPE._decode(data[decoded:], endianness)
                        self[i] = elem
                        decoded += elem_size
                return max(decoded, self._SIZE)

    return _array
