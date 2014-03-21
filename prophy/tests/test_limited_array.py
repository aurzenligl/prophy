import prophy
import pytest

class TestLimitedScalarArray():

    class Array(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("len", prophy.u32),
                       ("value", prophy.array(prophy.u32, size = 3, bound = "len"))]

    def test_assignment(self):
        a = self.Array()
        assert a.value == []
        a.value[:] = [1, 2, 3]
        assert a.value == [1, 2, 3]
        a.value[0] = 10
        assert a.value == [10, 2, 3]

        with pytest.raises(Exception):
            a.value.append(1)
        with pytest.raises(Exception):
            a.value.insert(0, 1)
        with pytest.raises(Exception):
            a.value[:] = [1, 2, 3, 4]
        with pytest.raises(Exception):
            a.value[1:2] = [1, 2, 3]

        b = self.Array()
        assert b.value[:] == []
        b.copy_from(a)
        assert b.value[:] == [10, 2, 3]

    def test_print(self):
        a = self.Array()
        a.value[:] = [1, 2]
        assert str(a) == ("value: 1\n"
                          "value: 2\n")
        a.value.append(3)
        assert str(a) == ("value: 1\n"
                          "value: 2\n"
                          "value: 3\n")

    def test_encode(self):
        a = self.Array()
        a.value[:] = [1, 2]
        assert a.encode(">") == "\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00"
        a.value[0] = 10
        assert a.encode(">") == "\x00\x00\x00\x02\x00\x00\x00\x0a\x00\x00\x00\x02\x00\x00\x00\x00"
        del a.value[1]
        assert a.encode(">") == "\x00\x00\x00\x01\x00\x00\x00\x0a\x00\x00\x00\x00\x00\x00\x00\x00"

    def test_decode(self):
        a = self.Array()
        a.decode("\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00", ">")
        assert a.value[:] == [1, 2]
        a.decode("\x00\x00\x00\x02\x00\x00\x00\x0a\x00\x00\x00\x02\x00\x00\x00\x00", ">")
        assert a.value[:] == [10, 2]
        a.decode("\x00\x00\x00\x01\x00\x00\x00\x0a\x00\x00\x00\x00\x00\x00\x00\x00", ">")
        assert a.value[:] == [10]
        a.decode("\x00\x00\x00\x00\x0f\x00\x00\x0a\x00\x02\x04\x05\x06\x07\x09\x00", ">")
        assert a.value[:] == []

        with pytest.raises(Exception):
            a.decode("\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01", ">")
        with pytest.raises(Exception):
            a.decode("\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00", ">")
        with pytest.raises(Exception):
            a.decode("\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00", ">")
        with pytest.raises(Exception):
            a.decode("\x00\x00\x00\x00", ">")

class TestLimitedCompositeArray():

    def test_exception(self):
        with pytest.raises(Exception):
            class Composite(prophy.struct):
                __metaclass__ = prophy.struct_generator
                _descriptor = [("x", prophy.array(prophy.u32, size = 2))]
            class Array(prophy.struct):
                __metaclass__ = prophy.struct_generator
                _descriptor = [("len", prophy.u32),
                               ("value", prophy.array(Composite, size = 2, bound = "len"))]
