# License

import sys

if sys.version > '3':
    long = int
    ifilter = filter
    xrange = range
else:
    long = long
    from itertools import ifilter

def cmp(a, b):
    return (a > b) - (a < b)

def with_metaclass(meta, *bases):
    class metaclass(meta):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})
