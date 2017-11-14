import prophy
import pytest

@pytest.fixture(scope = 'session')
def LimitedScalarArray():
    class LimitedScalarArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("len", prophy.u32),
                       ("value", prophy.array(prophy.u32, size = 3, bound = "len"))]
    return LimitedScalarArray

@pytest.fixture(scope = 'session')
def Composite():
    class Composite(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", prophy.u32),
                       ("y", prophy.u32)]
    return Composite

@pytest.fixture(scope = 'session')
def LimitedCompositeArray(Composite):
    class LimitedCompositeArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("len", prophy.u32),
                       ("value", prophy.array(Composite, size = 3, bound = "len"))]
    return LimitedCompositeArray

def test_limited_scalar_array_assignment(LimitedScalarArray):
    a = LimitedScalarArray()
    assert a.value == []
    a.value[:] = [1, 2, 3]
    assert a.value == [1, 2, 3]
    a.value[0] = 10
    assert a.value == [10, 2, 3]

    with pytest.raises(prophy.ProphyError) as err:
        a.value.append(1)
    assert str(err.value) == "exceeded array limit"
    with pytest.raises(prophy.ProphyError) as err:
        a.value.extend([1])
    assert str(err.value) == "exceeded array limit"
    with pytest.raises(prophy.ProphyError) as err:
        a.value.insert(0, 1)
    assert str(err.value) == "exceeded array limit"
    with pytest.raises(prophy.ProphyError) as err:
        a.value[:] = [1, 2, 3, 4]
    assert str(err.value) == "exceeded array limit"
    with pytest.raises(prophy.ProphyError) as err:
        a.value[1:2] = [1, 2, 3]
    assert str(err.value) == "exceeded array limit"

    b = LimitedScalarArray()
    b.value[:] == [9, 9]
    b.copy_from(a)
    assert b.value[:] == [10, 2, 3]
    b.copy_from(b)
    assert b.value == [10, 2, 3]

def test_limited_scalar_array_print(LimitedScalarArray):
    a = LimitedScalarArray()
    a.value[:] = [1, 2]
    assert str(a) == ("value: 1\n"
                      "value: 2\n")

def test_limited_scalar_array_encode(LimitedScalarArray):
    a = LimitedScalarArray()
    a.value[:] = [1, 2]
    assert a.encode(">") == b"\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00"

def test_limited_scalar_array_decode(LimitedScalarArray):
    a = LimitedScalarArray()
    a.decode(b"\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00", ">")
    assert a.value[:] == [1, 2]

    with pytest.raises(prophy.ProphyError) as e:
        a.decode(b"\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01", ">")
    assert 'exceeded array limit' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        a.decode(b"\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00", ">")
    assert 'too few bytes to decode array' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        a.decode(b"\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00", ">")
    assert 'not all bytes of LimitedScalarArray read' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        a.decode(b"\x00\x00\x00\x00", ">")
    assert 'too few bytes to decode array' in str(e.value)

def test_limited_composite_array_assigment(LimitedCompositeArray, Composite):
    a = LimitedCompositeArray()
    c = Composite()

    assert len(a.value) == 0
    b = a.value.add()

    assert str(a) == ("value {\n"
                      "  x: 0\n"
                      "  y: 0\n"
                      "}\n")

    b.x = 0x10
    b.y = 0x20
    assert len(a.value) == 1
    assert str(a) == ("value {\n"
                      "  x: 16\n"
                      "  y: 32\n"
                      "}\n")

    c.x = 5
    a.value.extend([c] * 2)
    assert len(a.value) == 3
    assert str(a) == ("value {\n"
                      "  x: 16\n"
                      "  y: 32\n"
                      "}\n"
                      "value {\n"
                      "  x: 5\n"
                      "  y: 0\n"
                      "}\n"
                      "value {\n"
                      "  x: 5\n"
                      "  y: 0\n"
                      "}\n")

def test_limited_composite_array_exception(LimitedCompositeArray, Composite):
    a = LimitedCompositeArray()
    c = Composite()

    with pytest.raises(prophy.ProphyError) as e:
        a.value.extend([c] * 4)
    assert "exceeded array limit" == str(e.value)

    a.value.extend([c] * 3)
    assert len(a.value) == 3

    with pytest.raises(prophy.ProphyError) as e:
        a.value.add()
    assert "exceeded array limit" == str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        a.decode((b"\x00\x00\x00\x04"
                  b"\x00\x00\x00\x22\x00\x00\x00\x13"
                  b"\x00\x00\x00\x22\x00\x00\x00\x13"
                  b"\x00\x00\x00\x22\x00\x00\x00\x13"
                  b"\x00\x00\x00\x33\x00\x00\x00\x14"), ">")
    assert "LimitedCompositeArray: exceeded array limit" == str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        a.decode((b"\x00\x00\x00\x03"
                  b"\x00\x00\x00\x22\x00\x00\x00\x13"
                  b"\x00\x00\x00\x22\x00\x00\x00\x13"
                  b"\x00\x00\x00\x22\x00\x00\x00\x13"
                  b"\x00"), ">")
    assert "not all bytes of LimitedCompositeArray read" == str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        a.decode((b"\x00\x00\x00\x00"), ">")
    assert "LimitedCompositeArray: too few bytes to decode array" == str(e.value)

def test_limited_composite_array_encode(LimitedCompositeArray, Composite):
    a = LimitedCompositeArray()
    assert a.encode(">") == (b"\x00\x00\x00\x00"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00")

    a.value.add()
    assert a.encode(">") == (b"\x00\x00\x00\x01"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00")
    a.value[0].x = 5
    assert a.encode(">") == (b"\x00\x00\x00\x01"
                             b"\x00\x00\x00\x05"b"\x00\x00\x00\x00"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00")
    assert a.encode("<") == (b"\x01\x00\x00\x00"
                             b"\x05\x00\x00\x00"b"\x00\x00\x00\x00"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"
                             b"\x00\x00\x00\x00"b"\x00\x00\x00\x00")

    c = Composite()
    c.x = 0x11
    a.value.extend([c] * 2)
    assert a.encode(">") == (b"\x00\x00\x00\x03"
                             b"\x00\x00\x00\x05\x00\x00\x00\x00"
                             b"\x00\x00\x00\x11\x00\x00\x00\x00"
                             b"\x00\x00\x00\x11\x00\x00\x00\x00")

    assert a.encode("<") == (b"\x03\x00\x00\x00"
                             b"\x05\x00\x00\x00\x00\x00\x00\x00"
                             b"\x11\x00\x00\x00\x00\x00\x00\x00"
                             b"\x11\x00\x00\x00\x00\x00\x00\x00")

def test_limited_composite_array_decode(LimitedCompositeArray):
    a = LimitedCompositeArray()

    a.decode((b"\x00\x00\x00\x01"
              b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"
              b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"
              b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"), ">")
    assert a.value[0].x == 0
    assert a.value[0].y == 0
    assert len(a.value) == 1

    a.decode((b"\x00\x00\x00\x02"
              b"\x00\x00\x00\x22"b"\x00\x00\x00\x13"
              b"\x00\x00\x00\x33"b"\x00\x00\x00\x14"
              b"\x00\x00\x00\x00"b"\x00\x00\x00\x00"), ">")

    assert len(a.value) == 2
    assert a.value[0].x == 0x22
    assert a.value[0].y == 0x13
    assert a.value[1].x == 0x33
    assert a.value[1].y == 0x14

    a.decode((b"\x03\x00\x00\x00"
              b"\x11\x00\x00\x00\x19\x00\x00\x00"
              b"\x22\x00\x00\x00\x29\x00\x00\x00"
              b"\x33\x00\x00\x00\x39\x00\x00\x00"), "<")

    assert len(a.value) == 3
    assert a.value[0].x == 0x11
    assert a.value[0].y == 0x19
    assert a.value[1].x == 0x22
    assert a.value[1].y == 0x29
    assert a.value[2].x == 0x33
    assert a.value[2].y == 0x39

def test_limited_array_with_enum():
    class E(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
        _enumerators = [("E_1", 1),
                        ("E_2", 2),
                        ("E_3", 3)]

    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("a_len", prophy.u32),
                       ("a", prophy.array(E, size = 3, bound = "a_len"))]

    x = A()

    assert b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" == x.encode(">")

    x.a.append(2)
    x.a.append("E_3")

    assert b"\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x00" == x.encode(">")

    x.decode(b"\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00", ">")

    assert [3, 1] == x.a[:]

def test_limited_array_with_field_afterwards():
    class S(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a", prophy.u8)]

    class A(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("a_len", prophy.u8),
                       ("a", prophy.array(S, size = 3, bound = "a_len")),
                       ("b", prophy.u8)]

    x = A()

    assert b"\x00\x00\x00\x00\x00" == x.encode(">")

    x.decode(b"\x02\x01\x02\x00\x03", ">")

    assert """\
a {
  a: 1
}
a {
  a: 2
}
b: 3
""" == str(x)
