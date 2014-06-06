import prophy
import pytest

@pytest.fixture(scope = 'session')
def FixedBytes():
    class FixedBytes(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value", prophy.bytes(size = 5))]
    return FixedBytes

def test_fixed_bytes_assignment(FixedBytes):
    x = FixedBytes()
    assert x.value == "\x00\x00\x00\x00\x00"

    x.value = "\x00\x00\x01"
    assert x.value == "\x00\x00\x01\x00\x00"

    x.value = "\x00\x00"
    assert x.value == "\x00\x00\x00\x00\x00"

    x.value = "bytes"
    assert x.value == "bytes"

    x.value = "bts"
    assert x.value == "bts\x00\x00"

    with pytest.raises(Exception) as e:
        x.value = 3
    assert e.value.message == 'not a str'

    with pytest.raises(Exception) as e:
        x.value = "123456"
    assert e.value.message == 'too long'

def test_fixed_bytes_copy_from(FixedBytes):
    x = FixedBytes()
    x.value = 'bts'
    y = FixedBytes()
    y.value = 'rotor'

    y.copy_from(x)
    assert y.value == "bts\x00\x00"

def test_fixed_bytes_encoding(FixedBytes):
    x = FixedBytes()
    x.value = "abc\x00"
    assert str(x) == "value: \'abc\\x00\\x00\'\n"

    assert x.encode(">") == "abc\x00\x00"

    x.value = "\x01"
    assert x.encode(">") == "\x01\x00\x00\x00\x00"

    x.decode("abc\x00\x00", ">")
    assert x.value == "abc\x00\x00"

    with pytest.raises(Exception):
        x.decode("\x01\x00\x00\x00\x00\x00", ">")

    with pytest.raises(Exception):
        x.decode("\x01\x00\x00\x00", ">")

def test_fixed_bytes_twice_in_struct():
    class X(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x", prophy.bytes(size = 5)),
                       ("y", prophy.bytes(size = 5))]
    x = X()
    x.x = "abcde"
    x.y = "fghij"
    assert str(x) == """\
x: 'abcde'
y: 'fghij'
"""

    assert x.encode(">") == "abcdefghij"

    x.decode("abcdefghij", ">")
    assert x.x == "abcde"
    assert x.y == "fghij"

@pytest.fixture(scope = 'session')
def BoundBytes():
    class BoundBytes(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value_len", prophy.u32),
                       ("value", prophy.bytes(bound = "value_len"))]
    return BoundBytes

def test_bound_bytes_assignment(BoundBytes):
    x = BoundBytes()
    assert x.value == ""

    x.value = "\x00\x00\x01"
    assert x.value == "\x00\x00\x01"

    x.value = "\x00\x00"
    assert x.value == "\x00\x00"

    x.value = "bytes"
    assert x.value == "bytes"

    x.value = "bts"
    assert x.value == "bts"

    with pytest.raises(Exception):
        x.value = 3

def test_bound_bytes_copy_from(BoundBytes):
    x = BoundBytes()
    x.value = 'bts'
    y = BoundBytes()
    y.value = 'rotor'

    y.copy_from(x)
    assert y.value == "bts"

def test_bound_bytes_encoding(BoundBytes):
    x = BoundBytes()
    x.value = "abc"
    assert str(x) == "value: \'abc\'\n"

    x.value = "\x00\x01"
    assert str(x) == "value: \'\\x00\\x01\'\n"

    x.value = "ab\x00"
    assert str(x) == "value: \'ab\\x00\'\n"

    x.value = "abc"
    assert x.encode(">") == "\x00\x00\x00\x03abc"

    x.value = "\x01"
    assert x.encode(">") == "\x00\x00\x00\x01\x01"

    x.decode("\x00\x00\x00\x03abc", ">")
    assert x.value == "abc"

    x.decode("\x00\x00\x00\x01\x01", ">")
    assert x.value == "\x01"

def test_bound_bytes_twice_in_struct():
    class X(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x_len", prophy.u32),
                       ("y_len", prophy.u32),
                       ("x", prophy.bytes(bound = "x_len")),
                       ("y", prophy.bytes(bound = "y_len"))]
    x = X()
    x.x = "abcde"
    x.y = "fghij"
    assert str(x) == ("x: \'abcde\'\n"
                      "y: \'fghij\'\n")
    assert x.encode(">") == "\x00\x00\x00\x05\x00\x00\x00\x05abcdefghij"

    x.decode("\x00\x00\x00\x05\x00\x00\x00\x05abcdefghij", ">")
    assert x.x == "abcde"
    assert x.y == "fghij"

@pytest.fixture(scope = 'session')
def ShiftBoundBytes():
    class ShiftBoundBytes(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value_len", prophy.u8),
                       ("value", prophy.bytes(bound = "value_len", shift = 2))]
    return ShiftBoundBytes

def test_shift_bound_bytes_encoding(ShiftBoundBytes):
    x = ShiftBoundBytes()
    x.value = "abc"
    assert x.encode(">") == "\x05abc"

    x.value = "\x01"
    assert x.encode(">") == "\x03\x01"

    x.decode("\x05abc", ">")
    assert x.value == "abc"

    x.decode("\x03\x01", ">")
    assert x.value == "\x01"

def test_shift_bound_bytes_encoding_exceptions(ShiftBoundBytes):
    x = ShiftBoundBytes()

    with pytest.raises(Exception) as e:
        x.decode("\x01", ">")
    assert e.value.message == "decoded array length smaller than shift"

    with pytest.raises(Exception) as e:
        x.decode("\x05", ">")
    assert e.value.message == "too few bytes to decode string"

    with pytest.raises(Exception) as e:
        x.decode("\x02\x00", ">")
    assert e.value.message == "not all bytes read"

def test_shift_bound_bytes_exceptions():
    with pytest.raises(Exception) as e:
        class Bytes(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("value_len", prophy.u8),
                           ("value", prophy.bytes(shift = 2))]
    assert e.value.message == "only shifting bound bytes implemented"

    with pytest.raises(Exception) as e:
        class Bytes(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("value_len", prophy.u8),
                           ("value", prophy.bytes(size = 1, shift = 2))]
    assert e.value.message == "only shifting bound bytes implemented"

    with pytest.raises(Exception) as e:
        class Bytes(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("value_len", prophy.u8),
                           ("value", prophy.bytes(bound = "value_len", size = 1, shift = 2))]
    assert e.value.message == "only shifting bound bytes implemented"

@pytest.fixture(scope = 'session')
def LimitedBytes():
    class LimitedBytes(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value_len", prophy.u32),
                       ("value", prophy.bytes(size = 5, bound = "value_len"))]
    return LimitedBytes

def test_limited_bytes_assignment(LimitedBytes):
    x = LimitedBytes()
    assert x.value == ""

    x.value = "\x00\x00\x01"
    assert x.value == "\x00\x00\x01"

    x.value = "\x00\x00"
    assert x.value == "\x00\x00"

    x.value = "bytes"
    assert x.value == "bytes"

    x.value = "bts"
    assert x.value == "bts"

    with pytest.raises(Exception):
        x.value = 3
    with pytest.raises(Exception):
        x.value = "123456"

def test_limited_bytes_copy_from(LimitedBytes):
    x = LimitedBytes()
    x.value = "bts"
    y = LimitedBytes()
    y.value = "rotor"

    y.copy_from(x)
    assert y.value == "bts"

def test_limited_bytes_encoding(LimitedBytes):
    x = LimitedBytes()
    x.value = "abc"
    assert str(x) == "value: \'abc\'\n"
    x.value = "\x00\x01"
    assert str(x) == "value: \'\\x00\\x01\'\n"
    x.value = "ab\x00"
    assert str(x) == "value: \'ab\\x00\'\n"

    x.value = "abc"
    assert x.encode(">") == "\x00\x00\x00\x03abc\x00\x00"
    x.value = "\x01"
    assert x.encode(">") == "\x00\x00\x00\x01\x01\x00\x00\x00\x00"

    x.decode("\x00\x00\x00\x03abc\x00\x00", ">")
    assert x.value == "abc"

    x.decode("\x00\x00\x00\x01\x01\x00\x00\x00\x00", ">")
    assert x.value == "\x01"

def test_limited_bytes_twice_in_struct():
    class X(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x_len", prophy.u32),
                       ("y_len", prophy.u32),
                       ("x", prophy.bytes(size = 5, bound = "x_len")),
                       ("y", prophy.bytes(size = 5, bound = "y_len"))]
    x = X()
    x.x = "abc"
    x.y = "efgh"
    assert str(x) == ("x: \'abc\'\n"
                      "y: \'efgh\'\n")
    assert x.encode(">") == "\x00\x00\x00\x03\x00\x00\x00\x04abc\x00\x00efgh\x00"

    x.decode("\x00\x00\x00\x02\x00\x00\x00\x03ab\x00\x00\x00fgh\x00\x00", ">")
    assert x.x == "ab"
    assert x.y == "fgh"

@pytest.fixture(scope = 'session')
def GreedyBytes():
    class GreedyBytes(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value", prophy.bytes())]
    return GreedyBytes

def test_greedy_bytes_assignment(GreedyBytes):
    x = GreedyBytes()
    assert x.value == ""
    x.value = "\x00\x00\x01"
    assert x.value == "\x00\x00\x01"
    x.value = "\x00\x00"
    assert x.value == "\x00\x00"
    x.value = "bytes"
    assert x.value == "bytes"
    x.value = "bts"
    assert x.value == "bts"

    with pytest.raises(Exception):
        x.value = 3

def test_greedy_bytes_copy_from(GreedyBytes):
    x = GreedyBytes()
    x.value = "bts"
    y = GreedyBytes()
    y.value = "rotor"

    y.copy_from(x)
    assert y.value == "bts"

def test_greedy_bytes_encoding(GreedyBytes):
    x = GreedyBytes()
    x.value = "abc"
    assert str(x) == "value: \'abc\'\n"
    x.value = "\x00\x01"
    assert str(x) == "value: \'\\x00\\x01\'\n"
    x.value = "ab\x00"
    assert str(x) == "value: \'ab\\x00\'\n"

    x.value = "abc"
    assert x.encode(">") == "abc"
    x.value = "\x01"
    assert x.encode(">") == "\x01"

    x.decode("abc", ">")
    assert x.value == "abc"
    x.decode("\x01", ">")
    assert x.value == "\x01"

def test_greedy_bytes_as_last_field():
    class X(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x", prophy.u32),
                       ("y", prophy.bytes())]
    x = X()
    x.x = 1
    x.y = "fgh"
    assert str(x) == ("x: 1\n"
                      "y: \'fgh\'\n")
    assert x.encode(">") == "\x00\x00\x00\x01fgh"

    x.decode("\x00\x00\x00\x01fgh", ">")
    assert x.x == 1
    assert x.y == "fgh"

def test_greedy_bytes_not_last_exceptions():
    with pytest.raises(Exception):
        class LastGreedyBytes(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", prophy.bytes()),
                           ("y", prophy.u32)]
    with pytest.raises(Exception):
        class X(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", prophy.u32),
                           ("y", prophy.bytes())]
        class Y(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", X),
                           ("y", prophy.u32)]
    with pytest.raises(Exception):
        class X(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", prophy.u32),
                           ("y", prophy.bytes())]
        class Y(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", prophy.u32),
                           ("y", prophy.array(X, size = 2))]
    with pytest.raises(Exception):
        class X(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", prophy.u32),
                           ("y", prophy.bytes())]
        class Y(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", prophy.u32),
                           ("y", X)]
        class Z(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", Y),
                           ("y", X)]

def test_greedy_bytes_in_array_exceptions():
    with pytest.raises(Exception):
        class X(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", prophy.array(prophy.bytes(size = 2), size = 2))]
    with pytest.raises(Exception):
        class X(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("z", prophy.u32),
                           ("y", prophy.u32),
                           ("x", prophy.array(prophy.bytes(bound = "y"), bound = "z"))]

def test_array_of_bytes_exceptions():
    with pytest.raises(Exception):
        class Bytes(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("value", prophy.array(prophy.bytes(size = 5), size = 5))]
    with pytest.raises(Exception):
        class Bytes(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("value_len", prophy.u32),
                           ("value", prophy.array(prophy.bytes(size = 5), bound = "value_len"))]
