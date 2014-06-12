import prophy
import pytest

@pytest.fixture(scope = 'session')
def Struct():
    class Struct(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x", prophy.u32),
                       ("y", prophy.u32)]
    return Struct

@pytest.fixture(scope = 'session')
def NestedStruct(Struct):
    class NestedStruct(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", Struct),
                       ("b", Struct)]
    return NestedStruct

@pytest.fixture(scope = 'session')
def DeeplyNestedStruct(NestedStruct, Struct):
    class DeeplyNestedStruct(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("m", NestedStruct),
                       ("n", Struct),
                       ("o", prophy.u32)]
    return DeeplyNestedStruct

def test_struct_assignment(Struct):
    x = Struct()

    assert x.x == 0
    assert x.y == 0
    x.x = 3
    x.y = 5

    with pytest.raises(Exception):
        x.nonexistent
    with pytest.raises(Exception):
        x.nonexistent = 10

    y = Struct()
    y.x = 9
    y.y = 9
    y.copy_from(x)
    assert y.x == 3
    assert y.y == 5

    with pytest.raises(Exception):
        y.copy_from("123")
    with pytest.raises(Exception):
        y.copy_from(123)

def test_struct_print(Struct):
    x = Struct()
    x.x = 1
    x.y = 2
    assert str(x) == ("x: 1\n"
                      "y: 2\n")

def test_struct_encode(Struct):
    x = Struct()
    x.x = 1
    x.y = 2
    assert x.encode(">") == ("\x00\x00\x00\x01"
                             "\x00\x00\x00\x02")

def test_struct_decode(Struct):
    x = Struct()
    x.decode(("\x00\x00\x00\x01"
              "\x00\x00\x00\x02"), ">")
    assert x.x == 1
    assert x.y == 2

def test_nested_struct_assignment(NestedStruct):
    x = NestedStruct()
    assert x.a.x == 0
    assert x.a.y == 0
    assert x.b.x == 0
    assert x.b.y == 0
    x.a.x = 1
    x.a.y = 2
    x.b.x = 3
    x.b.y = 4
    assert x.a.x == 1
    assert x.a.y == 2
    assert x.b.x == 3
    assert x.b.y == 4

    y = NestedStruct()
    y.a.x == 8
    y.a.y == 7
    y.b.x == 6
    y.b.y == 5
    y.copy_from(x)
    assert y.a.x == 1
    assert y.a.y == 2
    assert y.b.x == 3
    assert y.b.y == 4

def test_nested_struct_print(NestedStruct):
    y = NestedStruct()
    y.a.x = 1
    y.a.y = 2
    y.b.x = 3
    y.b.y = 4
    assert str(y) == ("a {\n"
                      "  x: 1\n"
                      "  y: 2\n"
                      "}\n"
                      "b {\n"
                      "  x: 3\n"
                      "  y: 4\n"
                      "}\n"
                      )

def test_nested_struct_encode(NestedStruct):
    y = NestedStruct()
    y.a.x = 1
    y.a.y = 2
    y.b.x = 3
    y.b.y = 4
    assert y.encode(">") == ("\x00\x00\x00\x01"
                             "\x00\x00\x00\x02"
                             "\x00\x00\x00\x03"
                             "\x00\x00\x00\x04")

def test_nested_struct_decode(NestedStruct):
    y = NestedStruct()
    y.decode(("\x00\x00\x00\x01"
              "\x00\x00\x00\x02"
              "\x00\x00\x00\x03"
              "\x00\x00\x00\x04"), ">")
    assert y.a.x == 1
    assert y.a.y == 2
    assert y.b.x == 3
    assert y.b.y == 4

def test_deeply_nested_struct_assignment(DeeplyNestedStruct):
    x = DeeplyNestedStruct()
    assert x.m.a.x == 0
    assert x.m.a.y == 0
    assert x.m.b.x == 0
    assert x.m.b.y == 0
    assert x.n.x == 0
    assert x.n.y == 0
    assert x.o == 0
    x.m.a.x = 1
    x.m.a.y = 2
    x.m.b.x = 3
    x.m.b.y = 4
    x.n.x = 5
    x.n.y = 6
    x.o = 7
    assert x.m.a.x == 1
    assert x.m.a.y == 2
    assert x.m.b.x == 3
    assert x.m.b.y == 4
    assert x.n.x == 5
    assert x.n.y == 6
    assert x.o == 7

    with pytest.raises(Exception):
        x.m = 10

    y = DeeplyNestedStruct()
    y.m.a.x = 8
    y.m.a.y = 7
    y.m.b.x = 6
    y.m.b.y = 5
    y.n.x = 4
    y.n.y = 3
    y.o = 2
    y.copy_from(x)
    assert y.m.a.x == 1
    assert y.m.a.y == 2
    assert y.m.b.x == 3
    assert y.m.b.y == 4
    assert y.n.x == 5
    assert y.n.y == 6
    assert y.o == 7

def test_deeply_nested_struct_print(DeeplyNestedStruct):
    z = DeeplyNestedStruct()
    z.m.a.x = 1
    z.m.a.y = 2
    z.m.b.x = 3
    z.m.b.y = 4
    z.n.x = 5
    z.n.y = 6
    z.o = 7
    assert str(z) == ("m {\n"
                      "  a {\n"
                      "    x: 1\n"
                      "    y: 2\n"
                      "  }\n"
                      "  b {\n"
                      "    x: 3\n"
                      "    y: 4\n"
                      "  }\n"
                      "}\n"
                      "n {\n"
                      "  x: 5\n"
                      "  y: 6\n"
                      "}\n"
                      "o: 7\n")

def test_deeply_nested_struct_encode(DeeplyNestedStruct):
    z = DeeplyNestedStruct()
    z.m.a.x = 1
    z.m.a.y = 2
    z.m.b.x = 3
    z.m.b.y = 4
    z.n.x = 5
    z.n.y = 6
    z.o = 7
    assert z.encode(">") == ("\x00\x00\x00\x01"
                             "\x00\x00\x00\x02"
                             "\x00\x00\x00\x03"
                             "\x00\x00\x00\x04"
                             "\x00\x00\x00\x05"
                             "\x00\x00\x00\x06"
                             "\x00\x00\x00\x07")

def test_deeply_nested_struct_decode(DeeplyNestedStruct):
    z = DeeplyNestedStruct()
    z.decode(("\x00\x00\x00\x01"
              "\x00\x00\x00\x02"
              "\x00\x00\x00\x03"
              "\x00\x00\x00\x04"
              "\x00\x00\x00\x05"
              "\x00\x00\x00\x06"
              "\x00\x00\x00\x07"), ">")
    assert z.m.a.x == 1
    assert z.m.a.y == 2
    assert z.m.b.x == 3
    assert z.m.b.y == 4
    assert z.n.x == 5
    assert z.n.y == 6
    assert z.o == 7

def test_empty_struct():
    class Empty(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = []

    x = Empty()

    assert "" == str(x)
    assert "" == x.encode(">")
    assert 0 == x.decode("", ">")

    class X(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("a", Empty)]

    x = X()

    assert """\
a {

}
""" == str(x)
    assert "" == x.encode(">")
    assert 0 == x.decode("", ">")
