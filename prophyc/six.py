import sys

if sys.version < '3':
    from itertools import ifilter
    reduce = reduce
    string_types = (str, unicode)

else:
    ifilter = filter
    from functools import reduce
    string_types = str
