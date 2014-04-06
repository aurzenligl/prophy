import prophy
import pytest

class X(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [("x", prophy.u32)]

class TestFixedScalarArray():

    class Array(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value", prophy.array(prophy.u32, size = 2))]

    def test_assignment(self):
        x = self.Array()
        assert x.value[:] == [0, 0]
        x.value[0] = 1
        x.value[1] = 2
        assert x.value[:] == [1, 2]
        x.value[:] = [6, 7]
        assert x.value[:] == [6, 7]

        with pytest.raises(Exception):
            del x.value[0]
        with pytest.raises(Exception):
            x.value.no_such_attribute
        with pytest.raises(Exception):
            x.value.no_such_attribute = 10
        with pytest.raises(Exception):
            x.value = 10
        with pytest.raises(Exception):
            x.value[:] = 10
        with pytest.raises(Exception):
            x.value[:] = (10,)
        with pytest.raises(Exception):
            x.value[0] = "will fail type check"
        with pytest.raises(Exception):
            x.value[0] = -1

        y = self.Array()
        assert y.value[:] == [0, 0]
        y.copy_from(x)
        assert y.value[:] == [6, 7]

    def test_print(self):
        x = self.Array()
        x.value[:] = [1, 2]
        assert str(x) == ("value: 1\n"
                          "value: 2\n")

    def test_encode(self):
        x = self.Array()
        x.value[:] = [1, 2]
        assert x.encode(">") == "\x00\x00\x00\x01\x00\x00\x00\x02"

    def test_decode(self):
        x = self.Array()
        x.decode("\x00\x00\x00\x01\x00\x00\x00\x02", ">")
        assert x.value[:] == [1, 2]

    def test_exception(self):
        class D(prophy.struct):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("a_len", prophy.u8),
                           ("a", prophy.array(prophy.u8, bound = "a_len"))]
        class U(prophy.struct):
            __metaclass__ = prophy.struct_generator
            _descriptor = [("a", prophy.array(prophy.u8))]

        with pytest.raises(Exception) as e:
            prophy.array(D, size = 2)
        assert "static/limited array of dynamic type not allowed" == e.value.message

        with pytest.raises(Exception) as e:
            prophy.array(U, size = 2)
        assert "static/limited array of dynamic type not allowed" == e.value.message

        with pytest.raises(Exception) as e:
            prophy.array(D, bound = "a_len", size = 2)
        assert "static/limited array of dynamic type not allowed" == e.value.message

        with pytest.raises(Exception) as e:
            prophy.array(U, bound = "a_len", size = 2)
        assert "static/limited array of dynamic type not allowed" == e.value.message

class TestFixedCompositeArray():

    class Array(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value", prophy.array(X, size = 2))]

    def test_assignment(self):
        x = self.Array()
        assert len(x.value) == 2
        assert x.value[0].x == 0
        assert x.value[1].x == 0
        x.value[0].x = 1
        assert x.value[0].x == 1
        x.value[1].x = 2
        assert x.value[1].x == 2

        y = self.Array()
        assert len(y.value) == 2
        assert y.value[0].x == 0
        assert y.value[1].x == 0
        y.copy_from(x)
        assert len(y.value) == 2
        assert y.value[0].x == 1
        assert y.value[1].x == 2

    def test_print(self):
        x = self.Array()
        x.value[0].x = 1
        x.value[1].x = 2
        assert str(x) == ("value {\n"
                          "  x: 1\n"
                          "}\n"
                          "value {\n"
                          "  x: 2\n"
                          "}\n")

    def test_encode(self):
        x = self.Array()
        x.value[0].x = 1
        x.value[1].x = 2
        assert x.encode(">") == "\x00\x00\x00\x01\x00\x00\x00\x02"

    def test_decode(self):
        x = self.Array()
        x.decode("\x00\x00\x00\x01\x00\x00\x00\x02", ">")
        assert x.value[0].x == 1
        assert x.value[1].x == 2
