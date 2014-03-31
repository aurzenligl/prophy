import prophy
import pytest

def test_union():
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u32, 0),
                       ("b", prophy.u32, 1),
                       ("c", prophy.u32, 2)]

    u = U()

    assert 'a: 0\n' == str(u)
    assert '\x00\x00\x00\x00\x00\x00\x00\x00' == u.encode(">")

    u.decode('\x02\x00\x00\x00\x10\x00\x00\x00', "<")

    assert 16 == u.c
