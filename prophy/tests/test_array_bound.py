import prophy
import pytest

@pytest.fixture(scope = 'session')
def BoundScalarArray():
    class BoundScalarArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("len", prophy.u32),
                       ("value", prophy.array(prophy.u32, bound = "len"))]
    return BoundScalarArray

@pytest.fixture(scope = 'session')
def BoundCompositeArray(BoundScalarArray):
    class BoundCompositeArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("len", prophy.u32),
                       ("value", prophy.array(BoundScalarArray, bound = "len"))]
    return BoundCompositeArray

def test_bound_scalar_array_assignment(BoundScalarArray):
    x = BoundScalarArray()
    assert x.value == []
    assert x.value[:] == []

    x.value[:] = [1, 2]
    assert x.value[:] == [1, 2]

    x.value[:] = [6, 7]
    assert x.value == [6, 7]
    assert x.value[:] == [6, 7]

    del x.value[1]
    assert x.value[:] == [6]

    x.value.insert(0, 23)
    assert x.value[:] == [23, 6]
    x.value.remove(23)
    assert x.value == [6]

    x.value[slice(0, 1)] = [123]
    assert x.value == [123]

    del x.value[:]
    assert x.value == []

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

def test_bound_scalar_array_copy_from(BoundScalarArray):
    x = BoundScalarArray()
    x.value[:] = [1, 2]
    y = BoundScalarArray()
    y.value[:] = [5, 6, 7]  # initial value to override

    y.copy_from(x)
    assert y.value[:] == [1, 2]

def test_bound_scalar_array_encoding(BoundScalarArray):
    x = BoundScalarArray()
    x.value[:] = [1, 2]

    assert x.encode(">") == b"\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02"

    assert str(x) == ("value: 1\n"
                      "value: 2\n")

    x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02", ">")
    assert x.value[:] == [1, 2]

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00", ">")
    assert 'too few bytes to decode integer' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00", ">")
    assert 'not all bytes of BoundScalarArray read' in str(e.value)

def test_bound_scalar_array_exceptions():
    with pytest.raises(Exception):
        class LengthFieldNonexistent(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a", prophy.array(prophy.i32, bound = "nonexistent"))]
    with pytest.raises(Exception):
        class LengthFieldAfter(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a", prophy.array(prophy.i32, bound = "after")),
                           ("after", prophy.i32)]
    with pytest.raises(Exception):
        class LengthFieldIsNotAnInteger(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("not_an_int", "not_an_int"),
                           ("a", prophy.array(prophy.i32, bound = "not_an_int"))]

def test_bound_scalar_array_twice_in_struct():
    class X2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("b_len", prophy.u8),
                       ("a_len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "a_len")),
                       ("b", prophy.array(prophy.u8, bound = "b_len"))]

    x = X2()

    x.a[:] = [1, 2, 3]
    x.b[:] = [6, 7]
    assert b"\x02\x03\x01\x02\x03\x06\x07" == x.encode(">")

    x.decode(b"\x01\x02\x07\x08\x01", ">")
    assert [7, 8] == x.a[:]
    assert [1] == x.b[:]

def test_bound_scalar_array_with_shift():
    class XS(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("len", prophy.u8),
                       ("value", prophy.array(prophy.u8, bound = "len", shift = 2))]

    x = XS()
    x.value[:] = [1, 2, 3, 4]

    assert x.encode(">") == b"\x06\x01\x02\x03\x04"

    x.decode(b"\x06\x01\x02\x03\x04", ">")
    assert x.value[:] == [1, 2, 3, 4]

    with pytest.raises(Exception) as e:
        x.decode(b"\x01", ">")
    assert str(e.value) == "XS: decoded array length smaller than shift"

    with pytest.raises(Exception) as e:
        x.decode(b"\x05", ">")
    assert str(e.value) == "XS: too few bytes to decode integer"

    with pytest.raises(Exception) as e:
        x.decode(b"\x02\x00", ">")
    assert str(e.value) == "not all bytes of XS read"

@pytest.mark.parametrize('array_type', [
    'prophy.array(prophy.u8, shift = 2)',
    'prophy.array(prophy.u8, size = 1, shift = 2)',
    'prophy.array(prophy.u8, bound = "value_len", size = 1, shift = 2)'
])
def test_bound_scalar_array_with_shift_exceptions(array_type):
    with pytest.raises(Exception) as e:
        exec(array_type)
    assert str(e.value) == "only shifting bound array implemented"

def test_bound_scalar_array_extend(BoundScalarArray):
    x = BoundScalarArray()
    x.value.extend([1, 2])
    assert x.value == [1, 2]
    x.value.extend([])
    assert x.value == [1, 2]

def test_bound_composite_array_assignment(BoundScalarArray, BoundCompositeArray):
    x = BoundCompositeArray()
    assert len(x.value) == 0

    x.value.add().value[:] = [1, 2]
    assert len(x.value) == 1
    assert x.value[0].value[:] == [1, 2]

    inner = BoundScalarArray()
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

    with pytest.raises(AttributeError):
        x.value.len
    with pytest.raises(AttributeError):
        x.value.len = 10
    with pytest.raises(prophy.ProphyError):
        x.value = 10
    with pytest.raises(TypeError):
        x.value.extend(1)
    with pytest.raises(TypeError):
        x.value.extend([1])
    with pytest.raises(Exception):
        x.value[:] = 1
    with pytest.raises(Exception):
        x.value[:] = [1]
    with pytest.raises(Exception):
        x.value[0] = 5

def test_bound_composite_array_copy_from(BoundCompositeArray):
    x = BoundCompositeArray()
    x.value.add().value[:] = [1, 2]
    x.value.add().value[:] = [3]
    y = BoundCompositeArray()
    y.value.add()
    y.value.add()
    y.value.add()  # initial value to override

    y.copy_from(x)
    assert len(y.value) == 2
    assert y.value[0].value[:] == [1, 2]
    assert y.value[1].value[:] == [3]

    y.copy_from(BoundCompositeArray())
    assert len(y.value) == 0

def test_bound_composite_array_add():
    class SubType(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("some", prophy.u32),
                       ("value", prophy.array(prophy.u32, size = 2))]

    class BoundCompositeArray_(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("len", prophy.u32),
                       ("value", prophy.array(SubType, bound = "len"))]

    a = BoundCompositeArray_()
    a.value.add(some = 543)
    assert a.value[0].some == 543

def test_bound_composite_array_encoding(BoundCompositeArray):
    x = BoundCompositeArray()
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

    assert x.encode(">") == (b"\x00\x00\x00\x02\x00\x00\x00\x02"
                             b"\x00\x00\x00\x01\x00\x00\x00\x02"
                             b"\x00\x00\x00\x01\x00\x00\x00\x03")

    x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x02"
             b"\x00\x00\x00\x01\x00\x00\x00\x02"
             b"\x00\x00\x00\x01\x00\x00\x00\x03", ">")
    assert len(x.value) == 2
    assert x.value[0].value[:] == [1, 2]
    assert x.value[1].value[:] == [3]

    x.decode(b"\x00\x00\x00\x00", ">")
    assert len(x.value) == 0

    with pytest.raises(Exception):
        x.decode(b"\x02\x00\x00\x00", ">")
    with pytest.raises(Exception):
        x.decode(b"\x00\x00\x00", ">")
    with pytest.raises(Exception):
        x.decode(b"\x00\x00\x00\x00\x00", ">")

def test_bound_composite_array_decode_multiple():
    class Y(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('x', prophy.u8)]

    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('num_of_x', prophy.u8),
                       ('x', prophy.array(Y, bound = 'num_of_x')),
                       ('num_of_y', prophy.u8),
                       ('y', prophy.array(Y, bound = 'num_of_y')),
                       ('num_of_z', prophy.u8),
                       ('z', prophy.array(Y, bound = 'num_of_z'))]

    x = X()
    x.decode(b'\x01\x00\x01\x00\x01\x00', '<')

def test_bound_composite_add_via_kwargs(BoundCompositeArray):
    x = BoundCompositeArray()
    x.value.add(value=[1])
    x.value.add(value=[2, 3])

    assert len(x.value) == 2
    assert x.value[0].value[:] == [1]
    assert x.value[1].value[:] == [2, 3]
