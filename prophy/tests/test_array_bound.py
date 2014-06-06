import prophy
import pytest

@pytest.fixture(scope = 'session')
def X():
    class X(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("len", prophy.u32),
                       ("value", prophy.array(prophy.u32, bound = "len"))]
    return X

@pytest.fixture(scope = 'session')
def Y(X):
    class Y(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("len", prophy.u32),
                       ("value", prophy.array(X, bound = "len"))]
    return Y

def test_bound_scalar_array_assignment(X):
    x = X()
    assert x.value == []
    assert x.value[:] == []

    x.value[:] = [1, 2]
    assert x.value[:] == [1, 2]

    x.value[:] = [6, 7]
    assert x.value == [6, 7]
    assert x.value[:] == [6, 7]

    del x.value[1]
    assert x.value[:] == [6]

    with pytest.raises(Exception):
        x.value.len
    with pytest.raises(Exception):
        x.value.len = 10
    with pytest.raises(Exception):
        x.value = 10
    with pytest.raises(Exception):
        x.value[0] = "will fail type check"
    with pytest.raises(Exception):
        x.value[0] = -1
    with pytest.raises(Exception):
        x.value[:] = [1, 2, "abc"]

def test_bound_scalar_array_copy_from(X):
    x = X()
    x.value[:] = [1, 2]
    y = X()
    y.value[:] = [5, 6, 7] # initial value to override

    y.copy_from(x)
    assert y.value[:] == [1, 2]

def test_bound_scalar_array_encoding(X):
    x = X()
    x.value[:] = [1, 2]

    assert x.encode(">") == "\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02"

    assert str(x) == ("value: 1\n"
                      "value: 2\n")

    x.decode("\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02", ">")
    assert x.value[:] == [1, 2]

    with pytest.raises(prophy.ProphyError) as e:
        x.decode("\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00", ">")
    assert 'too few bytes to decode integer' in e.value.message

    with pytest.raises(prophy.ProphyError) as e:
        x.decode("\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00", ">")
    assert 'not all bytes read' in e.value.message

def test_bound_scalar_array_exceptions():
    with pytest.raises(Exception):
        class LengthFieldNonexistent(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("a", prophy.array(prophy.i32, bound = "nonexistent"))]
    with pytest.raises(Exception):
        class LengthFieldAfter(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("a", prophy.array(prophy.i32, bound = "after")),
                           ("after", prophy.i32)]
    with pytest.raises(Exception):
        class LengthFieldIsNotAnInteger(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("not_an_int", "not_an_int"),
                           ("a", prophy.array(prophy.i32, bound = "not_an_int"))]

def test_bound_scalar_array_twice_in_struct():
    class X2(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("b_len", prophy.u8),
                       ("a_len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "a_len")),
                       ("b", prophy.array(prophy.u8, bound = "b_len"))]

    x = X2()

    x.a[:] = [1, 2, 3]
    x.b[:] = [6, 7]
    assert "\x02\x03\x01\x02\x03\x06\x07" == x.encode(">")

    x.decode("\x01\x02\x07\x08\x01", ">")
    assert [7, 8] == x.a[:]
    assert [1] == x.b[:]

def test_bound_scalar_array_with_shift():
    class XS(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("len", prophy.u8),
                       ("value", prophy.array(prophy.u8, bound = "len", shift = 2))]

    x = XS()
    x.value[:] = [1, 2, 3, 4]

    assert x.encode(">") == "\x06\x01\x02\x03\x04"

    x.decode("\x06\x01\x02\x03\x04", ">")
    assert x.value[:] == [1, 2, 3, 4]

    with pytest.raises(Exception) as e:
        x.decode("\x01", ">")
    assert e.value.message == "decoded array length smaller than shift"

    with pytest.raises(Exception) as e:
        x.decode("\x05", ">")
    assert e.value.message == "too few bytes to decode integer"

    with pytest.raises(Exception) as e:
        x.decode("\x02\x00", ">")
    assert e.value.message == "not all bytes read"

def test_bound_scalar_array_with_shift_exceptions():
    with pytest.raises(Exception) as e:
        class Array(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("value_len", prophy.u8),
                           ("value", prophy.array(prophy.u8, shift = 2))]
    assert e.value.message == "only shifting bound array implemented"
    with pytest.raises(Exception) as e:
        class Array(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("value_len", prophy.u8),
                           ("value", prophy.array(prophy.u8, size = 1, shift = 2))]
    assert e.value.message == "only shifting bound array implemented"
    with pytest.raises(Exception) as e:
        class Array(prophy.struct_packed):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("value_len", prophy.u8),
                           ("value", prophy.array(prophy.u8, bound = "value_len", size = 1, shift = 2))]
    assert e.value.message == "only shifting bound array implemented"

def test_bound_composite_array_assignment(X, Y):
    x = Y()
    assert len(x.value) == 0

    x.value.add().value[:] = [1, 2]
    assert len(x.value) == 1
    assert x.value[0].value[:] == [1, 2]

    inner = X()
    inner.value[:] = [3]
    x.value.extend([inner] * 2)
    assert len(x.value) == 3
    assert x.value[0].value[:] == [1, 2]
    assert x.value[1].value[:] == [3]
    assert x.value[2].value[:] == [3]

    x.value[1].value[0] = 10
    assert len(x.value) == 3
    assert x.value[0].value[:] == [1, 2]
    assert x.value[1].value[:] == [10]
    assert x.value[2].value[:] == [3]

    del x.value[1]
    assert len(x.value) == 2
    assert x.value[0].value[:] == [1, 2]
    assert x.value[1].value[:] == [3]

    with pytest.raises(Exception):
        x.value.len
    with pytest.raises(Exception):
        x.value.len = 10
    with pytest.raises(Exception):
        x.value = 10
    with pytest.raises(Exception):
        x.value.extend(1)
    with pytest.raises(Exception):
        x.value.extend([1])
    with pytest.raises(Exception):
        x.value[:] = 1
    with pytest.raises(Exception):
        x.value[:] = [1]
    with pytest.raises(Exception):
        x.value[0] = 5

def test_bound_composite_array_copy_from(Y):
    x = Y()
    x.value.add().value[:] = [1, 2]
    x.value.add().value[:] = [3]
    y = Y()
    y.value.add()
    y.value.add()
    y.value.add() # initial value to override

    y.copy_from(x)
    assert len(y.value) == 2
    assert y.value[0].value[:] == [1, 2]
    assert y.value[1].value[:] == [3]

    y.copy_from(Y())
    assert len(y.value) == 0

def test_bound_composite_array_encoding(Y):
    x = Y()
    x.value.add().value[:] = [1, 2]
    x.value.add().value[:] = [3]

    assert str(x) == """\
value {
  value: 1
  value: 2
}
value {
  value: 3
}
"""

    assert x.encode(">") == "\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03"

    x.decode("\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03", ">")
    assert len(x.value) == 2
    assert x.value[0].value[:] == [1, 2]
    assert x.value[1].value[:] == [3]

    x.decode("\x00\x00\x00\x00", ">")
    assert len(x.value) == 0

    with pytest.raises(Exception):
        x.decode("\x02\x00\x00\x00", ">")
    with pytest.raises(Exception):
        x.decode("\x00\x00\x00", ">")
    with pytest.raises(Exception):
        x.decode("\x00\x00\x00\x00\x00", ">")
