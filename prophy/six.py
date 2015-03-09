# License

import sys

if sys.version < '3':
    long = long
    from itertools import ifilter

    def b(x):
        return x
else:
    long = int
    ifilter = filter
    xrange = range

    def b(x):
        return x.decode()

def cmp(a, b):
    return (a > b) - (a < b)

def with_metaclass(meta, *bases):
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})
