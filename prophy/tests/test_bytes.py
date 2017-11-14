import prophy
import pytest

@pytest.fixture(scope = 'session')
def FixedBytes():
    class FixedBytes(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", prophy.bytes(size = 5))]
    return FixedBytes

@pytest.fixture(scope = 'session')
def BoundBytes():
    class BoundBytes(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value_len", prophy.u32),
                       ("value", prophy.bytes(bound = "value_len"))]
    return BoundBytes

@pytest.fixture(scope = 'session')
def ShiftBoundBytes():
    class ShiftBoundBytes(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value_len", prophy.u8),
                       ("value", prophy.bytes(bound = "value_len", shift = 2))]
    return ShiftBoundBytes

@pytest.fixture(scope = 'session')
def LimitedBytes():
    class LimitedBytes(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value_len", prophy.u32),
                       ("value", prophy.bytes(size = 5, bound = "value_len"))]
    return LimitedBytes

@pytest.fixture(scope = 'session')
def GreedyBytes():
    class GreedyBytes(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("value", prophy.bytes())]
    return GreedyBytes

def test_fixed_bytes_assignment(FixedBytes):
    x = FixedBytes()
    assert x.value == b"\x00\x00\x00\x00\x00"

    x.value = b"\x00\x00\x01"
    assert x.value == b"\x00\x00\x01\x00\x00"

    x.value = b"\x00\x00"
    assert x.value == b"\x00\x00\x00\x00\x00"

    x.value = b"bytes"
    assert x.value == b"bytes"

    x.value = b"bts"
    assert x.value == b"bts\x00\x00"

    with pytest.raises(Exception) as e:
        x.value = 3
    assert str(e.value) == 'not a bytes'

    with pytest.raises(Exception) as e:
        x.value = b"123456"
    assert str(e.value) == 'too long'

def test_fixed_bytes_copy_from(FixedBytes):
    x = FixedBytes()
    x.value = b'bts'
    y = FixedBytes()
    y.value = b'rotor'

    y.copy_from(x)
    assert y.value == b"bts\x00\x00"

def test_fixed_bytes_encoding(FixedBytes):
    x = FixedBytes()
    x.value = b"abc\x00"
    assert str(x) == "value: \'abc\\x00\\x00\'\n"

    assert x.encode(">") == b"abc\x00\x00"

    x.value = b"\x01"
    assert x.encode(">") == b"\x01\x00\x00\x00\x00"

    x.decode(b"abc\x00\x00", ">")
    assert x.value == b"abc\x00\x00"

    with pytest.raises(Exception):
        x.decode(b"\x01\x00\x00\x00\x00\x00", ">")

    with pytest.raises(Exception):
        x.decode(b"\x01\x00\x00\x00", ">")

def test_fixed_bytes_twice_in_struct():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("x", prophy.bytes(size = 5)),
                       ("y", prophy.bytes(size = 5))]
    x = X()
    x.x = b"abcde"
    x.y = b"fghij"
    assert str(x) == """\
x: 'abcde'
y: 'fghij'
"""

    assert x.encode(">") == b"abcdefghij"

    x.decode(b"abcdefghij", ">")
    assert x.x == b"abcde"
    assert x.y == b"fghij"

def test_bound_bytes_assignment(BoundBytes):
    x = BoundBytes()
    assert x.value == ""

    x.value = b"\x00\x00\x01"
    assert x.value == b"\x00\x00\x01"

    x.value = b"\x00\x00"
    assert x.value == b"\x00\x00"

    x.value = b"bytes"
    assert x.value == b"bytes"

    x.value = b"bts"
    assert x.value == b"bts"

    with pytest.raises(Exception):
        x.value = 3

def test_bound_bytes_copy_from(BoundBytes):
    x = BoundBytes()
    x.value = b'bts'
    y = BoundBytes()
    y.value = b'rotor'

    y.copy_from(x)
    assert y.value == b"bts"

def test_bound_bytes_encoding(BoundBytes):
    x = BoundBytes()
    x.value = b"abc"
    assert str(x) == "value: \'abc\'\n"

    x.value = b"\x00\x01"
    assert str(x) == "value: \'\\x00\\x01\'\n"

    x.value = b"ab\x00"
    assert str(x) == "value: \'ab\\x00\'\n"

    x.value = b"abc"
    assert x.encode(">") == b"\x00\x00\x00\x03abc"

    x.value = b"\x01"
    assert x.encode(">") == b"\x00\x00\x00\x01\x01"

    x.decode(b"\x00\x00\x00\x03abc", ">")
    assert x.value == b"abc"

    x.decode(b"\x00\x00\x00\x01\x01", ">")
    assert x.value == b"\x01"

def test_bound_bytes_twice_in_struct():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("x_len", prophy.u32),
                       ("y_len", prophy.u32),
                       ("x", prophy.bytes(bound = "x_len")),
                       ("y", prophy.bytes(bound = "y_len"))]
    x = X()
    x.x = b"abcde"
    x.y = b"fghij"
    assert str(x) == ("x: \'abcde\'\n"
                      "y: \'fghij\'\n")
    assert x.encode(">") == b"\x00\x00\x00\x05\x00\x00\x00\x05abcdefghij"

    x.decode(b"\x00\x00\x00\x05\x00\x00\x00\x05abcdefghij", ">")
    assert x.x == b"abcde"
    assert x.y == b"fghij"

def test_shift_bound_bytes_encoding(ShiftBoundBytes):
    x = ShiftBoundBytes()
    x.value = b"abc"
    assert x.encode(">") == b"\x05abc"

    x.value = b"\x01"
    assert x.encode(">") == b"\x03\x01"

    x.decode(b"\x05abc", ">")
    assert x.value == b"abc"

    x.decode(b"\x03\x01", ">")
    assert x.value == b"\x01"

def test_shift_bound_bytes_encoding_exceptions(ShiftBoundBytes):
    x = ShiftBoundBytes()

    with pytest.raises(Exception) as e:
        x.decode(b"\x01", ">")
    assert str(e.value) == "ShiftBoundBytes: decoded array length smaller than shift"

    with pytest.raises(Exception) as e:
        x.decode(b"\x05", ">")
    assert str(e.value) == "ShiftBoundBytes: too few bytes to decode string"

    with pytest.raises(Exception) as e:
        x.decode(b"\x02\x00", ">")
    assert str(e.value) == "not all bytes of ShiftBoundBytes read"

@pytest.mark.parametrize('bytes_type', [
    'prophy.bytes(shift = 2)',
    'prophy.bytes(size = 1, shift = 2)',
    'prophy.bytes(bound = "value_len", size = 1, shift = 2)'
])
def test_shift_bound_bytes_exceptions(bytes_type):
    with pytest.raises(Exception) as e:
        exec(bytes_type)
    assert str(e.value) == "only shifting bound bytes implemented"

def test_limited_bytes_assignment(LimitedBytes):
    x = LimitedBytes()
    assert x.value == ""

    x.value = b"\x00\x00\x01"
    assert x.value == b"\x00\x00\x01"

    x.value = b"\x00\x00"
    assert x.value == b"\x00\x00"

    x.value = b"bytes"
    assert x.value == b"bytes"

    x.value = b"bts"
    assert x.value == b"bts"

    with pytest.raises(Exception):
        x.value = 3
    with pytest.raises(Exception):
        x.value = b"123456"

def test_limited_bytes_copy_from(LimitedBytes):
    x = LimitedBytes()
    x.value = b"bts"
    y = LimitedBytes()
    y.value = b"rotor"

    y.copy_from(x)
    assert y.value == b"bts"

def test_limited_bytes_encoding(LimitedBytes):
    x = LimitedBytes()
    x.value = b"abc"
    assert str(x) == "value: \'abc\'\n"
    x.value = b"\x00\x01"
    assert str(x) == "value: \'\\x00\\x01\'\n"
    x.value = b"ab\x00"
    assert str(x) == "value: \'ab\\x00\'\n"

    x.value = b"abc"
    assert x.encode(">") == b"\x00\x00\x00\x03abc\x00\x00"
    x.value = b"\x01"
    assert x.encode(">") == b"\x00\x00\x00\x01\x01\x00\x00\x00\x00"

    x.decode(b"\x00\x00\x00\x03abc\x00\x00", ">")
    assert x.value == b"abc"

    x.decode(b"\x00\x00\x00\x01\x01\x00\x00\x00\x00", ">")
    assert x.value == b"\x01"

def test_limited_bytes_twice_in_struct():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("x_len", prophy.u32),
                       ("y_len", prophy.u32),
                       ("x", prophy.bytes(size = 5, bound = "x_len")),
                       ("y", prophy.bytes(size = 5, bound = "y_len"))]
    x = X()
    x.x = b"abc"
    x.y = b"efgh"
    assert str(x) == ("x: \'abc\'\n"
                      "y: \'efgh\'\n")
    assert x.encode(">") == b"\x00\x00\x00\x03\x00\x00\x00\x04abc\x00\x00efgh\x00"

    x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x03ab\x00\x00\x00fgh\x00\x00", ">")
    assert x.x == b"ab"
    assert x.y == b"fgh"

def test_greedy_bytes_assignment(GreedyBytes):
    x = GreedyBytes()
    assert x.value == ""
    x.value = b"\x00\x00\x01"
    assert x.value == b"\x00\x00\x01"
    x.value = b"\x00\x00"
    assert x.value == b"\x00\x00"
    x.value = b"bytes"
    assert x.value == b"bytes"
    x.value = b"bts"
    assert x.value == b"bts"

    with pytest.raises(Exception):
        x.value = 3

def test_greedy_bytes_copy_from(GreedyBytes):
    x = GreedyBytes()
    x.value = b"bts"
    y = GreedyBytes()
    y.value = b"rotor"

    y.copy_from(x)
    assert y.value == b"bts"

def test_greedy_bytes_encoding(GreedyBytes):
    x = GreedyBytes()
    x.value = b"abc"
    assert str(x) == "value: \'abc\'\n"
    x.value = b"\x00\x01"
    assert str(x) == "value: \'\\x00\\x01\'\n"
    x.value = b"ab\x00"
    assert str(x) == "value: \'ab\\x00\'\n"

    x.value = b"abc"
    assert x.encode(">") == b"abc"
    x.value = b"\x01"
    assert x.encode(">") == b"\x01"

    x.decode(b"abc", ">")
    assert x.value == b"abc"
    x.decode(b"\x01", ">")
    assert x.value == b"\x01"

def test_greedy_bytes_as_last_field():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("x", prophy.u32),
                       ("y", prophy.bytes())]
    x = X()
    x.x = 1
    x.y = b"fgh"
    assert str(x) == ("x: 1\n"
                      "y: \'fgh\'\n")
    assert x.encode(">") == b"\x00\x00\x00\x01fgh"

    x.decode(b"\x00\x00\x00\x01fgh", ">")
    assert x.x == 1
    assert x.y == b"fgh"

def test_greedy_bytes_not_last_exceptions():
    with pytest.raises(prophy.ProphyError):
        class LastGreedyBytes(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("x", prophy.bytes()),
                           ("y", prophy.u32)]
    with pytest.raises(prophy.ProphyError):
        class X1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("x", prophy.u32),
                           ("y", prophy.bytes())]

        class X2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("x", X1),
                           ("y", prophy.u32)]
    with pytest.raises(prophy.ProphyError):
        class Y1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("x", prophy.u32),
                           ("y", prophy.bytes())]

        class Y2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("x", prophy.u32),
                           ("y", prophy.array(Y1, size = 2))]
    with pytest.raises(prophy.ProphyError):
        class Z1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("x", prophy.u32),
                           ("y", prophy.bytes())]

        class Z2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("x", prophy.u32),
                           ("y", Z1)]

        class Z3(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("x", Z2),
                           ("y", Z1)]

@pytest.mark.parametrize('array_type', [
    'prophy.array(prophy.bytes(size = 5), size = 5)',
    'prophy.array(prophy.bytes(size = 5), bound = "value_len")',
    'prophy.array(prophy.bytes(bound = "y"), bound = "z")'
])
def test_array_of_bytes_not_allowed(array_type):
    with pytest.raises(prophy.ProphyError) as e:
        exec(array_type)
    assert str(e.value) == 'array of strings not allowed'

def test_bytes_non_7bit_ascii_to_string(FixedBytes):
    x = FixedBytes()
    x.value = b'\xff\x80\xbb'
    assert str(x) == "value: '\\xff\\x80\\xbb\\x00\\x00'\n"
