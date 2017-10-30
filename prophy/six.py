# License

import sys

if sys.version < '3':
    long = long
    from itertools import ifilter
    xrange = xrange

    def repr_bytes(x):
        return repr(x)

else:
    long = int
    ifilter = filter
    xrange = range

    def repr_bytes(x):
        return "'" + repr(x)[2:-1] + "'"


def with_metaclass(meta, *bases):
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})
