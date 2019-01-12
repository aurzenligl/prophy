import sys

if sys.version < '3':  # pragma: no cover
    from itertools import ifilter

    reduce = reduce
    string_types = (str, unicode)


    def to_bytes(str_):
        return str_


    def decode_string(str_or_unicode_or_bytes):
        if isinstance(str_or_unicode_or_bytes, str):
            if any(ord(c) > 127 for c in str_or_unicode_or_bytes):
                return str_or_unicode_or_bytes.decode("utf-8")
            return str_or_unicode_or_bytes
        if isinstance(str_or_unicode_or_bytes, bytes):
            return str_or_unicode_or_bytes.decode("utf-8")
        if isinstance(str_or_unicode_or_bytes, unicode):
            return str_or_unicode_or_bytes
        raise TypeError("Got text as %s, expected string." % type(str_or_unicode_or_bytes).__name__)

else:  # pragma: no cover
    ifilter = filter
    from functools import reduce

    string_types = (str,)


    def decode_string(str_or_bytes):
        if isinstance(str_or_bytes, bytes):
            return str_or_bytes.decode("utf-8")
        if isinstance(str_or_bytes, string_types):
            return str_or_bytes
        raise TypeError("Got text as %s, expected string." % type(str_or_bytes).__name__)


    def to_bytes(str_):
        return bytes(str_, 'utf-8')
