from prophy.scalar import prophy_data_object


class base_array(prophy_data_object):
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

    def sort(self, key_function=lambda x: x):
        self._values.sort(key=key_function)

    @classmethod
    def _bricks_walk(cls, cursor):

        if cls._max_len:
            indexes = range(cls._max_len)
        else:
            if not cls._UNLIMITED:

                size_info = "@%s" % cls._BOUND
                if cls._max_len:
                    size_info += " %s" % cls._max_len
            else:
                size_info = "..."

            indexes = [size_info]

        for index in indexes:
            for brick_type, brick_path in cls._TYPE._bricks_walk(cursor):
                path_ = "[%s]%s" % (index, brick_path or "")
                yield brick_type, path_

