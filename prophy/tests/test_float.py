import prophy
import pytest

class Testr32():

    class X(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value", prophy.r32)]

    def test(self):
        x = self.X()
        assert x.value == 0.0

        with pytest.raises(Exception):
            x.value = "45.486"

        y = self.X()
        assert y.value == 0.0

        x.value = 1.455
        y.copy_from(x)
        assert y.value == 1.455

    def test_codec(self):
        x = self.X()

        x.value = 8
        assert str(x) == "value: 8.0\n"


        x.decode("\x3f\x80\x00\x00", ">")
        assert x.value == 1.0

        x.decode("\xbf\x80\x00\x00", ">")
        assert x.value == -1.0

        x.value = -1.0
        assert x.encode(">") == "\xbf\x80\x00\x00"

        x.value = 1.0
        assert x.encode(">") == "\x3f\x80\x00\x00"

        with pytest.raises(Exception):
            x.decode("\xff\xff\xff\xff\xff", ">")

        with pytest.raises(Exception):
            x.decode("\xff\xff\xff", ">")

class Testr64():

    class X(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [("value", prophy.r64)]

    def test(self):
        x = self.X()
        assert x.value == 0.0

        with pytest.raises(Exception):
            x.value = "45.486"

        y = self.X()
        assert y.value == 0.0

        x.value = 1.455
        y.copy_from(x)
        assert y.value == 1.455

    def test_codec(self):
        x = self.X()

        x.value = 8
        assert str(x) == "value: 8.0\n"

        x.decode("\xbf\xf0\x00\x00\x00\x00\x00\x00", ">")
        assert x.value == -1.0

        x.value = -1.0
        assert x.encode(">") == "\xbf\xf0\x00\x00\x00\x00\x00\x00"

        with pytest.raises(Exception):
            x.decode("\xff\xff\xff\xff\xff", ">")

        with pytest.raises(Exception):
            x.decode("\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff", ">")