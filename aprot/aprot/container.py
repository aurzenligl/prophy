class base_array(object):
    __slots__ = ['_values']
    _tags = ["repeated"]
    
    def __init__(self):
        self._values = []
        
    def __getitem__(self, key):
        value = self._values[key]
        if "enum" in self._TYPE._tags:
            return self._TYPE._int_to_name[value]
        return value
    
    def __len__(self):
        return len(self._values)
    
    def __ne__(self, other):
        return not self == other
    
    def __hash__(self):
        raise TypeError('unhashable object')
    
    def __repr__(self):
        return repr(self._values)
    
    def sort(self, sort_function=cmp):
        self._values.sort(sort_function)
        
class fixed_scalar_array(base_array):
    
    __slots__ = []
    
    def __init__(self):
        super(fixed_scalar_array, self).__init__()
        self._values = [self._TYPE._DEFAULT] * self._SIZE
    
    def __setitem__(self, key, value):
        value = self._TYPE._checker.check(value)
        self._values[key] = value
    
    def __getslice__(self, start, stop):
        values = self._values[start:stop]
        if "enum" in self._TYPE._tags:
            int_to_name = self._TYPE._int_to_name
            values = [int_to_name[val] for val in values]
        return values
    
    def __setslice__(self, start, stop, values):
        if len(self._values[start:stop]) is not len(values):
            raise Exception("setting slice with different length collection")
        new_values = []
        for value in values:
            value = self._TYPE._checker.check(value)
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
        value = self._TYPE._checker.check(value)
        if self._LIMIT and len(self) == self._LIMIT:
            raise Exception("exceeded array limit")
        self._values.append(value)
        
    def insert(self, key, value):
        value = self._TYPE._checker.check(value)
        if self._LIMIT and len(self) == self._LIMIT:
            raise Exception("exceeded array limit")
        self._values.insert(key, value)
    
    def extend(self, elem_seq):
        if not elem_seq:
            return
        if self._LIMIT and len(self) + len(elem_seq) > self._LIMIT:
            raise Exception("exceeded array limit")
        new_values = []
        for elem in elem_seq:
            elem = self._TYPE._checker.check(elem)
            new_values.append(elem)
        self._values.extend(new_values)
    
    def remove(self, elem):
        self._values.remove(elem)
    
    def __setitem__(self, key, value):
        value = self._TYPE._checker.check(value)
        self._values[key] = value
    
    def __getslice__(self, start, stop):
        values = self._values[start:stop]
        if "enum" in self._TYPE._tags:
            int_to_name = self._TYPE._int_to_name
            values = [int_to_name[val] for val in values]
        return values
    
    def __setslice__(self, start, stop, values):
        if self._LIMIT and len(self) + len(values) - len(self._values[start:stop]) > self._LIMIT:
            raise Exception("exceeded array limit")
        new_values = []
        for value in values:
            value = self._TYPE._checker.check(value)
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
        self._values = [self._TYPE() for _ in range(self._SIZE)]

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
 
    # TODO kl. implement **kwargs to fill structure with data at addition time already
    def add(self):
        new_element = self._TYPE()
        self._values.append(new_element)
        return new_element

    def extend(self, elem_seq):
        composite_cls = self._TYPE
        values = self._values
        for message in elem_seq:
            new_element = composite_cls()
            new_element.copy_from(message)
            values.append(new_element)

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

def array(field_type, **kwargs):
    field_tags = field_type._tags
    if "repeated" in field_tags:
        raise Exception("array of arrays not allowed")
    elif "string" in field_tags:
        raise Exception("array of strings not allowed")
    if "shift" in kwargs and (not "bound" in kwargs or "size" in kwargs):
        raise Exception("only shifting bound array implemented")
    size = kwargs.pop("size", 0)
    bound = kwargs.pop("bound", "")
    shift = kwargs.pop("shift", 0)
    if kwargs:
        raise Exception("unknown arguments to array field")
    
    tags = []
    actual_size = size
    if size and bound:
        if "composite" in field_tags:
            raise Exception("limited composite array not supported")
        else:
            base = bound_scalar_array
    elif size and not bound:
        actual_size = 0
        if "composite" in field_tags:
            base = fixed_composite_array
        else:
            base = fixed_scalar_array
    elif not size and bound:
        if "composite" in field_tags:
            base = bound_composite_array
        else:
            base = bound_scalar_array
    elif not size and not bound:
        tags += ["greedy"]
        if "composite" in field_tags:
            base = bound_composite_array
        else:
            base = bound_scalar_array
    
    class concrete_array(base):
        __slots__ = []
        _tags = base._tags + tags 
        _TYPE = field_type
        _LIMIT = actual_size
        if size:
            _SIZE = size
        if bound:
            _LENGTH_FIELD = bound
            _LENGTH_SHIFT = shift
    return concrete_array
