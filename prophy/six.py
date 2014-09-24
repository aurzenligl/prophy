# License

import sys

if sys.version > '3':
    long = int
    ifilter = filter
else:
    long = long
    from itertools import ifilter

def cmp(a, b):
    return (a > b) - (a < b)
