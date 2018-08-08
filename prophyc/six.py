import sys

if sys.version < '3':  # pragma: no cover
    from itertools import ifilter
    reduce = reduce

    def to_bytes(str_):
        return str_

else:  # pragma: no cover
    ifilter = filter
    from functools import reduce

    def to_bytes(str_):
        return bytes(str_, 'utf-8')
