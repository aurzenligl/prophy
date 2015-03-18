import sys

if sys.version < '3':
    from itertools import ifilter
    reduce = reduce

else:
    ifilter = filter
    from functools import reduce
