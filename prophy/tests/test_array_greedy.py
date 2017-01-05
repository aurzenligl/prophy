import prophy
import pytest

@pytest.fixture(scope = 'session')
def GreedyScalarArray():
    class GreedyScalarArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", prophy.array(prophy.u32))]
    return GreedyScalarArray

@pytest.fixture(scope = 'session')
def Composite():
    class Composite(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", prophy.u16),
                       ("y", prophy.i16)]
    return Composite

@pytest.fixture(scope = 'session')
def GreedyCompositeArray(Composite):
    class GreedyCompositeArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("x", prophy.array(Composite))]
    return GreedyCompositeArray

@pytest.fixture(scope = 'session')
def ComplexComposite(Composite):
    class ComplexComposite(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("y_len", prophy.u32),
                       ("x", Composite),
                       ("y", prophy.array(Composite, bound = "y_len"))]
    return ComplexComposite

@pytest.fixture(scope = 'session')
def GreedyComplexCompositeArray(ComplexComposite):
    class GreedyComplexCompositeArray(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("x", prophy.array(ComplexComposite))]
    return GreedyComplexCompositeArray

def test_greedy_scalar_array_assignment(GreedyScalarArray):
    a = GreedyScalarArray()
    a.x[:] = [1, 2, 3, 4]
    assert a.x == [1, 2, 3, 4]
    a.x[0] = 10
    assert a.x == [10, 2, 3, 4]
    a.x[1:-1] = []
    assert a.x == [10, 4]

    b = GreedyScalarArray()
    b.x[:] = [1, 2, 3]
    b.copy_from(a)
    assert b.x[:] == [10, 4]

def test_greedy_scalar_array_print(GreedyScalarArray):
    a = GreedyScalarArray()
    a.x[:] = [1, 2, 3, 4]
    assert str(a) == ("x: 1\n"
                      "x: 2\n"
                      "x: 3\n"
                      "x: 4\n")

def test_greedy_scalar_array_encode(GreedyScalarArray):
    a = GreedyScalarArray()
    a.x[:] = [1, 2, 3, 4]
    assert a.encode(">") == b"\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04"

def test_greedy_scalar_array_decode(GreedyScalarArray):
    a = GreedyScalarArray()
    a.decode(b"\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04", ">")
    assert a.x[:] == [1, 2, 3, 4]

    with pytest.raises(prophy.ProphyError):
        a.decode(b"\x00\x00\x00\x0a\x00\x00\x00\x04\x00", ">")

def test_greedy_composite_array_assignment(GreedyCompositeArray, Composite):
    a = GreedyCompositeArray()
    c = Composite()
    c.x, c.y = 10, 20
    a.x.extend([c] * 2)
    assert len(a.x) == 2
    assert a.x[0].x == 10
    assert a.x[0].y == 20
    assert a.x[1].x == 10
    assert a.x[1].y == 20
    c = a.x.add()
    c.x, c.y = 1, -1
    assert a.x[2].x == 1
    assert a.x[2].y == -1

    b = GreedyCompositeArray()
    b.copy_from(a)
    assert len(b.x) == 3
    assert b.x[0].x == 10
    assert b.x[0].y == 20
    assert b.x[1].x == 10
    assert b.x[1].y == 20
    assert b.x[2].x == 1
    assert b.x[2].y == -1

def test_greedy_composite_array_print(GreedyCompositeArray, Composite):
    a = GreedyCompositeArray()
    c = Composite()
    c.x, c.y = 10, 20
    a.x.extend([c] * 2)
    assert str(a) == ("x {\n"
                      "  x: 10\n"
                      "  y: 20\n"
                      "}\n"
                      "x {\n"
                      "  x: 10\n"
                      "  y: 20\n"
                      "}\n")
    c = a.x.add()
    c.x, c.y = 1, -1
    assert str(a) == ("x {\n"
                      "  x: 10\n"
                      "  y: 20\n"
                      "}\n"
                      "x {\n"
                      "  x: 10\n"
                      "  y: 20\n"
                      "}\n"
                      "x {\n"
                      "  x: 1\n"
                      "  y: -1\n"
                      "}\n")

def test_greedy_composite_array_encode(GreedyCompositeArray, Composite):
    a = GreedyCompositeArray()
    c = Composite()
    c.x, c.y = 10, 20
    a.x.extend([c] * 2)
    assert a.encode(">") == b"\x00\x0a\x00\x14\x00\x0a\x00\x14"
    c = a.x.add()
    c.x, c.y = 1, -1
    assert a.encode(">") == b"\x00\x0a\x00\x14\x00\x0a\x00\x14\x00\x01\xff\xff"

def test_greedy_composite_array_decode(GreedyCompositeArray):
    a = GreedyCompositeArray()
    a.decode(b"\x00\x0a\x00\x14\x00\x0a\x00\x14", ">")
    assert len(a.x) == 2
    assert a.x[0].x == 10
    assert a.x[0].y == 20
    assert a.x[1].x == 10
    assert a.x[1].y == 20
    a.decode(b"\x00\x0a\x00\x14\x00\x0a\x00\x14\x00\x01\xff\xff", ">")
    assert len(a.x) == 3
    assert a.x[0].x == 10
    assert a.x[0].y == 20
    assert a.x[1].x == 10
    assert a.x[1].y == 20
    assert a.x[2].x == 1
    assert a.x[2].y == -1

    with pytest.raises(Exception):
        a.decode(b"\x00\x0a\x00\x14\x00\x0a\x00\x14\x00\x01\xff\xff\x00", ">")

def test_greedy_complex_composite_array_assignment(GreedyComplexCompositeArray):
    a = GreedyComplexCompositeArray()
    c = a.x.add()
    c.x.x, c.x.y = 1, 2
    cc = c.y.add()
    cc.x, cc.y = 3, 4
    cc = c.y.add()
    cc.x, cc.y = 5, 6
    assert len(a.x) == 1
    assert len(a.x[0].y) == 2
    assert a.x[0].x.x == 1
    assert a.x[0].x.y == 2
    assert a.x[0].y[0].x == 3
    assert a.x[0].y[0].y == 4
    assert a.x[0].y[1].x == 5
    assert a.x[0].y[1].y == 6
    c = a.x.add()
    c.x.x, c.x.y = 7, 8
    assert len(a.x) == 2
    assert len(a.x[0].y) == 2
    assert len(a.x[1].y) == 0
    assert a.x[0].x.x == 1
    assert a.x[0].x.y == 2
    assert a.x[0].y[0].x == 3
    assert a.x[0].y[0].y == 4
    assert a.x[0].y[1].x == 5
    assert a.x[0].y[1].y == 6
    assert a.x[1].x.x == 7
    assert a.x[1].x.y == 8

    b = GreedyComplexCompositeArray()
    b.copy_from(a)
    assert len(b.x) == 2
    assert len(b.x[0].y) == 2
    assert len(b.x[1].y) == 0
    assert b.x[0].x.x == 1
    assert b.x[0].x.y == 2
    assert b.x[0].y[0].x == 3
    assert b.x[0].y[0].y == 4
    assert b.x[0].y[1].x == 5
    assert b.x[0].y[1].y == 6
    assert b.x[1].x.x == 7
    assert b.x[1].x.y == 8

def test_greedy_complex_composite_array_print(GreedyComplexCompositeArray):
    a = GreedyComplexCompositeArray()
    c = a.x.add()
    c.x.x, c.x.y = 1, 2
    cc = c.y.add()
    cc.x, cc.y = 3, 4
    cc = c.y.add()
    cc.x, cc.y = 5, 6
    assert str(a) == ("x {\n"
                      "  x {\n"
                      "    x: 1\n"
                      "    y: 2\n"
                      "  }\n"
                      "  y {\n"
                      "    x: 3\n"
                      "    y: 4\n"
                      "  }\n"
                      "  y {\n"
                      "    x: 5\n"
                      "    y: 6\n"
                      "  }\n"
                      "}\n")
    c = a.x.add()
    c.x.x, c.x.y = 7, 8
    assert str(a) == ("x {\n"
                      "  x {\n"
                      "    x: 1\n"
                      "    y: 2\n"
                      "  }\n"
                      "  y {\n"
                      "    x: 3\n"
                      "    y: 4\n"
                      "  }\n"
                      "  y {\n"
                      "    x: 5\n"
                      "    y: 6\n"
                      "  }\n"
                      "}\n"
                      "x {\n"
                      "  x {\n"
                      "    x: 7\n"
                      "    y: 8\n"
                      "  }\n"
                      "}\n")

def test_greedy_complex_composite_array_encode(GreedyComplexCompositeArray):
    a = GreedyComplexCompositeArray()
    c = a.x.add()
    c.x.x, c.x.y = 1, 2
    cc = c.y.add()
    cc.x, cc.y = 3, 4
    cc = c.y.add()
    cc.x, cc.y = 5, 6
    assert a.encode(">") == b"\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06"
    c = a.x.add()
    c.x.x, c.x.y = 7, 8
    assert a.encode(">") == (b"\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04"
                             b"\x00\x05\x00\x06\x00\x00\x00\x00\x00\x07\x00\x08")

def test_greedy_complex_composite_array_decode(GreedyComplexCompositeArray):
    a = GreedyComplexCompositeArray()
    a.decode(b"\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06", ">")
    assert len(a.x) == 1
    assert len(a.x[0].y) == 2
    assert a.x[0].x.x == 1
    assert a.x[0].x.y == 2
    assert a.x[0].y[0].x == 3
    assert a.x[0].y[0].y == 4
    assert a.x[0].y[1].x == 5
    assert a.x[0].y[1].y == 6
    a.decode(b"\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06\x00\x00\x00\x00\x00\x07\x00\x08", ">")
    assert len(a.x) == 2
    assert len(a.x[0].y) == 2
    assert len(a.x[1].y) == 0
    assert a.x[0].x.x == 1
    assert a.x[0].x.y == 2
    assert a.x[0].y[0].x == 3
    assert a.x[0].y[0].y == 4
    assert a.x[0].y[1].x == 5
    assert a.x[0].y[1].y == 6
    assert a.x[1].x.x == 7
    assert a.x[1].x.y == 8

    with pytest.raises(Exception):
        a.decode(b"\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04"
                 b"\x00\x05\x00\x06\x00\x00\x00\x00\x00\x07\x00\x08\x00", ">")

def test_greedy_array_exceptions():
    with pytest.raises(Exception) as e:
        class NotLast(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("y", prophy.array(prophy.u32)),
                           ("x", prophy.u32)]
    assert "unlimited field is not the last one" == str(e.value)

    with pytest.raises(Exception) as e:
        class GreedyComposite(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("x", prophy.array(prophy.u32))]
        prophy.array(GreedyComposite)
    assert "array with unlimited field disallowed" == str(e.value)

def test_greedy_array_comparisons():
    class X(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("x", prophy.u32)]

    class Y(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("x", prophy.u32)]

    class Z(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("x", prophy.array(Y))]

    x1 = Z()
    x2 = Z()

    x1.x.add()

    with pytest.raises(prophy.ProphyError) as e:
        assert x1.x == [X()]
    assert 'Can only compare repeated composite fields against other repeated composite fields' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        assert x1.x == [Y()]
    assert 'Can only compare repeated composite fields against other repeated composite fields' in str(e.value)

    assert x1.x == x1.x
    assert x1.x != x2.x
