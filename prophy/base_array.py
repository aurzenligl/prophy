from .six import cmp

class base_array(object):
    __slots__ = ['_values']

    def __init__(self):
        self._values = []

    def __getitem__(self, idx):
        return self._values[idx]

    def __getslice__(self, start, stop):
        return self._values[start:stop]

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
