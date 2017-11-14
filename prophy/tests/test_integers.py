import prophy
import pytest

@pytest.mark.parametrize('IntType, min, max', [
    (prophy.i8, -(0x80), 0x7F),
    (prophy.i16, -(0x8000), 0x7FFF),
    (prophy.i32, -(0x80000000), 0x7FFFFFFF),
    (prophy.i64, -(0x8000000000000000), 0x7FFFFFFFFFFFFFFF),
    (prophy.u8, 0, 0xFF),
    (prophy.u16, 0, 0xFFFF),
    (prophy.u32, 0, 0xFFFFFFFF),
    (prophy.u64, 0, 0xFFFFFFFFFFFFFFFF)
])
def test_integer(IntType, min, max):
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("value", IntType)]

    x = X()
    assert x.value == 0
    x.value = max
    assert x.value == max
    x.value = min
    assert x.value == min

    with pytest.raises(prophy.ProphyError) as e:
        x.value = "123"
    assert "not an int" in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.value = max + 1
    assert "out of bounds" in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.value = min - 1
    assert "out of bounds" in str(e.value)

    y = X()
    y.value == 42
    y.copy_from(x)
    assert y.value == min

@pytest.mark.parametrize('IntType, a, encoded_a, b, encoded_b, too_short, too_long', [
    (prophy.i8,
        1, b"\x01",
        (-1), b"\xff",
        b"",
        b"\xff\xff"),
    (prophy.i16,
        1, b"\x00\x01",
        (-1), b"\xff\xff",
        b"\xff",
        b"\xff\xff\xff"),
    (prophy.i32,
        1, b"\x00\x00\x00\x01",
        (-1), b"\xff\xff\xff\xff",
        b"\xff\xff\xff",
        b"\xff\xff\xff\xff\xff"),
    (prophy.i64,
        1, b"\x00\x00\x00\x00\x00\x00\x00\x01",
        (-1), b"\xff\xff\xff\xff\xff\xff\xff\xff",
        b"\xff\xff\xff\xff\xff\xff\xff",
        b"\xff\xff\xff\xff\xff\xff\xff\xff\xff"),
    (prophy.u8,
        1, b"\x01",
        0, b"\x00",
        b"",
        b"\xff\xff"),
    (prophy.u16,
        1, b"\x00\x01",
        0, b"\x00\x00",
        b"\xff",
        b"\xff\xff\xff"),
    (prophy.u32,
        1, b"\x00\x00\x00\x01",
        0, b"\x00\x00\x00\x00",
        b"\xff\xff\xff",
        b"\xff\xff\xff\xff\xff"),
    (prophy.u64,
        1, b"\x00\x00\x00\x00\x00\x00\x00\x01",
        0, b"\x00\x00\x00\x00\x00\x00\x00\x00",
        b"\xff\xff\xff\xff\xff\xff\xff",
        b"\xff\xff\xff\xff\xff\xff\xff\xff\xff")
])
def test_integer_codec(IntType, a, encoded_a, b, encoded_b, too_short, too_long):
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("value", IntType)]

    x = X()
    x.value = 8
    assert str(x) == "value: 8\n"

    x.value = a
    assert x.encode(">") == encoded_a
    x.value = b
    assert x.encode(">") == encoded_b

    x.decode(encoded_a, ">")
    assert x.value == a
    x.decode(encoded_b, ">")
    assert x.value == b

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(too_short, ">")
    assert "too few bytes to decode integer" in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(too_long, ">")
    assert "not all bytes of {} read".format(X.__name__) in str(e.value)
