from . import composite
from .exception import ProphyError
from .base_array import base_array
from .six import *

def decode_scalar_array(tp, data, pos, endianness, count):
    if count is None:
        items, remainder = divmod(len(data) - pos, tp._SIZE)
        count = items + bool(remainder)
    cursor = 0
    values = []
    for _ in xrange(count):
        value, size = tp._decode(data, pos + cursor, endianness)
        cursor += size
        values.append(value)
    return values, cursor

def scalar_array_eq(self, other):
    if self is other:
        return True
    # Special case for the same type which should be common and fast.
    if isinstance(other, self.__class__):
        return other._values == self._values
    # We are presumably comparing against some other sequence type.
    return other == self._values

def composite_array_eq(self, other):
    if self is other:
        return True
    if not isinstance(other, self.__class__):
        raise ProphyError('Can only compare repeated composite fields against '
                          'other repeated composite fields.')
    return self._values == other._values

class fixed_scalar_array(base_array):
    __slots__ = []

    def __init__(self):
        super(fixed_scalar_array, self).__init__()
        self._values = [self._TYPE._DEFAULT] * self._max_len

    def __setitem__(self, idx, value):
        if isinstance(idx, slice):
            self.__setslice__(idx.start, idx.stop, value)
        else:
            value = self._TYPE._check(value)
            self._values[idx] = value

    def __setslice__(self, start, stop, values):
        if len(self._values[start:stop]) != len(values):
            raise ProphyError("setting slice with different length collection")
        self._values[start:stop] = map(self._TYPE._check, values)

    def __eq__(self, other):
        return scalar_array_eq(self, other)

    def _encode_impl(self, endianness):
        return b"".join(self._TYPE._encode(value, endianness) for value in self)

    def _decode_impl(self, data, pos, endianness, _):
        self[:], size = decode_scalar_array(self._TYPE, data, pos, endianness, len(self))
        return size

class bound_scalar_array(base_array):
    __slots__ = []

    def __init__(self):
        super(bound_scalar_array, self).__init__()

    def append(self, value):
        value = self._TYPE._check(value)
        if self._max_len and len(self) == self._max_len:
            raise ProphyError("exceeded array limit")
        self._values.append(value)

    def insert(self, idx, value):
        value = self._TYPE._check(value)
        if self._max_len and len(self) == self._max_len:
            raise ProphyError("exceeded array limit")
        self._values.insert(idx, value)

    def extend(self, values):
        if not values:
            return
        if self._max_len and len(self) + len(values) > self._max_len:
            raise ProphyError("exceeded array limit")
        self._values.extend(map(self._TYPE._check, values))

    def remove(self, elem):
        self._values.remove(elem)

    def __setitem__(self, idx, value):
        if isinstance(idx, slice):
            self.__setslice__(idx.start, idx.stop, value)
        else:
            value = self._TYPE._check(value)
            self._values[idx] = value

    def __setslice__(self, start, stop, values):
        if self._max_len and len(self) + len(values) - len(self._values[start:stop]) > self._max_len:
            raise ProphyError("exceeded array limit")
        self._values[start:stop] = map(self._TYPE._check, values)

    def __delitem__(self, idx):
        del self._values[idx]

    def __delslice__(self, start, stop):
        del self._values[start:stop]

    def __eq__(self, other):
        return scalar_array_eq(self, other)

    def _encode_impl(self, endianness):
        return b"".join(self._TYPE._encode(value, endianness) for value in self).ljust(self._SIZE, b"\x00")

    def _decode_impl(self, data, pos, endianness, len_hint):
        if self._SIZE > (len(data) - pos):
            raise ProphyError("too few bytes to decode array")
        self[:], size = decode_scalar_array(self._TYPE, data, pos, endianness, len_hint)
        return max(size, self._SIZE)

class fixed_composite_array(base_array):

    __slots__ = []

    def __init__(self):
        super(fixed_composite_array, self).__init__()
        self._values = [self._TYPE() for _ in xrange(self._max_len)]

    def __eq__(self, other):
        return composite_array_eq(self, other)

    def _encode_impl(self, endianness):
        return b"".join(value.encode(endianness, terminal = False) for value in self)

    def _decode_impl(self, data, pos, endianness, _):
        cursor = 0
        for elem in self:
            cursor += elem._decode_impl(data, pos + cursor, endianness, terminal = False)
        return cursor

class bound_composite_array(base_array):
    __slots__ = []

    def __init__(self):
        super(bound_composite_array, self).__init__()

    def add(self, **attributes):
        if self._max_len and len(self) == self._max_len:
            raise ProphyError("exceeded array limit")

        new_element = self._TYPE()
        self._values.append(new_element)
        for name, value in attributes.items():
            attr = getattr(new_element, name)
            if isinstance(attr, base_array):
                attr[:] = value
            else:
                setattr(new_element, name, value)
        return new_element

    def extend(self, elem_seq):
        if self._max_len and len(self) + len(elem_seq) > self._max_len:
            raise ProphyError("exceeded array limit")

        composite_cls = self._TYPE
        for message in elem_seq:
            new_element = composite_cls()
            new_element.copy_from(message)
            self._values.append(new_element)

    def __delitem__(self, idx):
        del self._values[idx]

    def __delslice__(self, start, stop):
        del self._values[start:stop]

    def __eq__(self, other):
        return composite_array_eq(self, other)

    def _encode_impl(self, endianness):
        return b"".join(value.encode(endianness, terminal = False) for value in self).ljust(self._SIZE, b"\x00")

    def _decode_impl(self, data, pos, endianness, len_hint):
        if self._SIZE > (len(data) - pos):
            raise ProphyError("too few bytes to decode array")
        del self[:]
        cursor = 0
        if not self._SIZE and not self._BOUND:
            while (pos + cursor) < len(data):
                cursor += self.add()._decode_impl(data, pos + cursor, endianness, terminal = False)
        else:
            for _ in xrange(len_hint):
                cursor += self.add()._decode_impl(data, pos + cursor, endianness, terminal = False)
        return max(cursor, self._SIZE)

def array(type_, **kwargs):
    size = kwargs.pop("size", 0)
    bound = kwargs.pop("bound", None)
    shift = kwargs.pop("shift", 0)
    if kwargs:
        raise ProphyError("unknown arguments to array field")

    if issubclass(type_, base_array):
        raise ProphyError("array of arrays not allowed")
    if issubclass(type_, bytes):
        raise ProphyError("array of strings not allowed")
    if size and type_._DYNAMIC:
        raise ProphyError("static/limited array of dynamic type not allowed")
    if shift and (not bound or size):
        raise ProphyError("only shifting bound array implemented")
    if type_._UNLIMITED:
        raise ProphyError("array with unlimited field disallowed")
    if type_._OPTIONAL:
        raise ProphyError("array of optional type not allowed")

    is_static = size and not bound
    is_composite = issubclass(type_, (composite.struct, composite.union))

    if is_composite:
        base = fixed_composite_array if is_static else bound_composite_array
    else:
        base = fixed_scalar_array if is_static else bound_scalar_array

    class _array(base):
        __slots__ = []
        _max_len = size
        _TYPE = type_
        _SIZE = size * type_._SIZE
        _DYNAMIC = not size
        _UNLIMITED = not size and not bound
        _OPTIONAL = False
        _ALIGNMENT = type_._ALIGNMENT
        _BOUND = bound
        _BOUND_SHIFT = shift
        _PARTIAL_ALIGNMENT = None

    return _array
