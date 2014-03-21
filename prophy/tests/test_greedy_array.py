import prophy
import pytest

class Composite(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("x", prophy.u16),
                   ("y", prophy.i16)]

class ComplexComposite(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("y_len", prophy.u32),
                   ("x", Composite),
                   ("y", prophy.array(Composite, bound = "y_len"))]

class TestGreedyScalarArray():

    class Array(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x", prophy.array(prophy.u32))]

    def test_assignment(self):
        a = self.Array()
        a.x[:] = [1, 2, 3, 4]
        assert a.x == [1, 2, 3, 4]
        a.x[0] = 10
        assert a.x == [10, 2, 3, 4]
        a.x[1:-1] = []
        assert a.x == [10, 4]

        b = self.Array()
        assert b.x[:] == []
        b.copy_from(a)
        assert b.x[:] == [10, 4]

    def test_print(self):
        a = self.Array()
        a.x[:] = [1, 2, 3, 4]
        assert str(a) == ("x: 1\n"
                          "x: 2\n"
                          "x: 3\n"
                          "x: 4\n")
        a.x[0] = 10
        assert str(a) == ("x: 10\n"
                          "x: 2\n"
                          "x: 3\n"
                          "x: 4\n")
        a.x[1:-1] = []
        assert str(a) == ("x: 10\n"
                          "x: 4\n")

    def test_encode(self):
        a = self.Array()
        a.x[:] = [1, 2, 3, 4]
        assert a.encode(">") == "\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04"
        a.x[0] = 10
        assert a.encode(">") == "\x00\x00\x00\x0a\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04"
        a.x[1:-1] = []
        assert a.encode(">") == "\x00\x00\x00\x0a\x00\x00\x00\x04"

    def test_decode(self):
        a = self.Array()
        a.decode("\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04", ">")
        assert a.x[:] == [1, 2, 3, 4]
        a.decode("\x00\x00\x00\x0a\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04", ">")
        assert a.x[:] == [10, 2, 3, 4]
        a.decode("\x00\x00\x00\x0a\x00\x00\x00\x04", ">")
        assert a.x[:] == [10, 4]

        with pytest.raises(Exception):
            a.decode("\x00\x00\x00\x0a\x00\x00\x00\x04\x00", ">")

class TestGreedyCompositeArray():

    class Array(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x", prophy.array(Composite))]

    def test_assignment(self):
        a = self.Array()
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

        b = self.Array()
        assert len(b.x) == 0
        b.copy_from(a)
        assert len(b.x) == 3
        assert b.x[0].x == 10
        assert b.x[0].y == 20
        assert b.x[1].x == 10
        assert b.x[1].y == 20
        assert b.x[2].x == 1
        assert b.x[2].y == -1

    def test_print(self):
        a = self.Array()
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

    def test_encode(self):
        a = self.Array()
        c = Composite()
        c.x, c.y = 10, 20
        a.x.extend([c] * 2)
        assert a.encode(">") == "\x00\x0a\x00\x14\x00\x0a\x00\x14"
        c = a.x.add()
        c.x, c.y = 1, -1
        assert a.encode(">") == "\x00\x0a\x00\x14\x00\x0a\x00\x14\x00\x01\xff\xff"

    def test_decode(self):
        a = self.Array()
        a.decode("\x00\x0a\x00\x14\x00\x0a\x00\x14", ">")
        assert len(a.x) == 2
        assert a.x[0].x == 10
        assert a.x[0].y == 20
        assert a.x[1].x == 10
        assert a.x[1].y == 20
        a.decode("\x00\x0a\x00\x14\x00\x0a\x00\x14\x00\x01\xff\xff", ">")
        assert len(a.x) == 3
        assert a.x[0].x == 10
        assert a.x[0].y == 20
        assert a.x[1].x == 10
        assert a.x[1].y == 20
        assert a.x[2].x == 1
        assert a.x[2].y == -1

        with pytest.raises(Exception):
            a.decode("\x00\x0a\x00\x14\x00\x0a\x00\x14\x00\x01\xff\xff\x00", ">")

class TestGreedyComplexCompositeArray():

    class Array(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("x", prophy.array(ComplexComposite))]

    def test_assignment(self):
        a = self.Array()
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

        b = self.Array()
        assert len(b.x) == 0
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

    def test_print(self):
        a = self.Array()
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

    def test_encode(self):
        a = self.Array()
        c = a.x.add()
        c.x.x, c.x.y = 1, 2
        cc = c.y.add()
        cc.x, cc.y = 3, 4
        cc = c.y.add()
        cc.x, cc.y = 5, 6
        assert a.encode(">") == "\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06"
        c = a.x.add()
        c.x.x, c.x.y = 7, 8
        assert a.encode(">") == "\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06\x00\x00\x00\x00\x00\x07\x00\x08"

    def test_decode(self):
        a = self.Array()
        a.decode("\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06", ">")
        assert len(a.x) == 1
        assert len(a.x[0].y) == 2
        assert a.x[0].x.x == 1
        assert a.x[0].x.y == 2
        assert a.x[0].y[0].x == 3
        assert a.x[0].y[0].y == 4
        assert a.x[0].y[1].x == 5
        assert a.x[0].y[1].y == 6
        a.decode("\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06\x00\x00\x00\x00\x00\x07\x00\x08", ">")
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
            a.decode("\x00\x00\x00\x02\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06\x00\x00\x00\x00\x00\x07\x00\x08\x00", ">")

def test_exceptions():
    with pytest.raises(Exception):
        class NotLast(prophy.struct):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("y", prophy.array(prophy.u32)),
                           ("x", prophy.u32)]
    with pytest.raises(Exception):
        class GreedyComposite(prophy.struct):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", prophy.array(prophy.u32))]
        class GreedyArrayOfGreedyComposites(prophy.struct):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("x", prophy.array(GreedyComposite))]
