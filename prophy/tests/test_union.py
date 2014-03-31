import prophy
import pytest

def make_U():
    class U(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [("a", prophy.u32, 0),
                       ("b", prophy.u32, 1),
                       ("c", prophy.u32, 2)]
    return U()

def test_simple_union():
    x = make_U()

    assert 0 == x.a
    assert 'a: 0\n' == str(x)
    assert '\x00\x00\x00\x00\x00\x00\x00\x00' == x.encode(">")

    x.decode('\x02\x00\x00\x00\x10\x00\x00\x00', "<")

    assert 16 == x.c
    assert 'c: 16\n' == str(x)
    assert '\x00\x00\x00\x02\x00\x00\x00\x10' == x.encode(">")

def test_simple_union_discriminator_initial_value():
    x = make_U()

    assert 0 == x.discriminator

def test_simple_union_discriminator_accepts_ints_or_field_name_and_clears():
    x = make_U()

    x.a = 42
    x.discriminator = 1

    assert 0 == x.b
    assert 'b: 0\n' == str(x)
    assert '\x00\x00\x00\x01\x00\x00\x00\x00' == x.encode(">")

    x.discriminator = "c"

    assert 0 == x.c
    assert 'c: 0\n' == str(x)
    assert '\x00\x00\x00\x02\x00\x00\x00\x00' == x.encode(">")

def test_simple_union_discriminator_does_not_clear_fields_if_set_to_same_value():
    x = make_U()

    x.a = 42

    x.discriminator = 0

    assert 42 == x.a

    x.discriminator = "a"

    assert 42 == x.a
