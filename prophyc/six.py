import sys

if sys.version < '3':  # pragma: no cover
    from itertools import ifilter
    reduce = reduce
    string_types = (str, unicode)

    def to_bytes(str_):
        return str_

else:  # pragma: no cover
    ifilter = filter
    from functools import reduce
    string_types = str

    def to_bytes(str_):
        return bytes(str_, 'utf-8')
