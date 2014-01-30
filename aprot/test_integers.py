import aprot
import pytest

class TestI8():

    class X(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.i8)]
    
    def test(self):
        x = self.X()
        assert x.value == 0
        x.value = 0x7F
        assert x.value == 0x7F
        x.value = -(0x80)
        assert x.value == -(0x80)
        
        with pytest.raises(Exception):
            x.value = "123"
        with pytest.raises(Exception):
            x.value = 0x7F + 1
        with pytest.raises(Exception):
            x.value = -(0x80) - 1
        
        y = self.X()
        assert y.value == 0
        y.copy_from(x)
        assert y.value == -(0x80)
    
    def test_codec(self):
        x = self.X()

        x.value = 8
        assert str(x) == "value: 8\n"
        
        x.value = 1
        assert x.encode(">") == "\x01"
        x.value = -1
        assert x.encode(">") == "\xff"

        x.decode("\x01", ">")
        assert x.value == 1
        x.decode("\xff", ">")
        assert x.value == -1
        
        with pytest.raises(Exception):
            x.decode("", ">")
        with pytest.raises(Exception):
            x.decode("\xff\xff", ">")

class TestI16():

    class X(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.i16)]

    def test(self):
        x = self.X()
        assert x.value == 0
        x.value = 0x7FFF
        assert x.value == 0x7FFF
        x.value = -(0x8000)
        assert x.value == -(0x8000)
        
        with pytest.raises(Exception):
            x.value = "123"
        with pytest.raises(Exception):
            x.value = 0x7FFF + 1
        with pytest.raises(Exception):
            x.value = -(0x8000) - 1
        
        y = self.X()
        assert y.value == 0
        y.copy_from(x)
        assert y.value == -(0x8000)
    
    def test_codec(self):
        x = self.X()

        x.value = 8
        assert str(x) == "value: 8\n"
        
        x.value = 1
        assert x.encode(">") == "\x00\x01"
        x.value = -1
        assert x.encode(">") == "\xff\xff"

        x.decode("\x00\x01", ">")
        assert x.value == 1
        x.decode("\xff\xff", ">")
        assert x.value == -1
        
        with pytest.raises(Exception):
            x.decode("\xff", ">")
        with pytest.raises(Exception):
            x.decode("\xff\xff\xff", ">")

class TestI32():

    class X(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.i32)]

    def test(self):
        x = self.X()
        assert x.value == 0
        x.value = 0x7FFFFFFF
        assert x.value == 0x7FFFFFFF
        x.value = -(0x80000000)
        assert x.value == -(0x80000000)
        
        with pytest.raises(Exception):
            x.value = "123"
        with pytest.raises(Exception):
            x.value = 0x7FFFFFFF + 1
        with pytest.raises(Exception):
            x.value = -(0x80000000) - 1
        
        y = self.X()
        assert y.value == 0
        y.copy_from(x)
        assert y.value == -(0x80000000)
    
    def test_codec(self):
        x = self.X()

        x.value = 8
        assert str(x) == "value: 8\n"
        
        x.value = 1
        assert x.encode(">") == "\x00\x00\x00\x01"
        x.value = -1
        assert x.encode(">") == "\xff\xff\xff\xff"

        x.decode("\x00\x00\x00\x01", ">")
        assert x.value == 1
        x.decode("\xff\xff\xff\xff", ">")
        assert x.value == -1
        
        with pytest.raises(Exception):
            x.decode("\xff\xff\xff", ">")
        with pytest.raises(Exception):
            x.decode("\xff\xff\xff\xff\xff", ">")

class TestI64():

    class X(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.i64)]

    def test(self):
        x = self.X()
        assert x.value == 0
        x.value = 0x7FFFFFFFFFFFFFFF
        assert x.value == 0x7FFFFFFFFFFFFFFF
        x.value = -(0x8000000000000000)
        assert x.value == -(0x8000000000000000)
        
        with pytest.raises(Exception):
            x.value = "123"
        with pytest.raises(Exception):
            x.value = 0x7FFFFFFFFFFFFFFF + 1
        with pytest.raises(Exception):
            x.value = -(0x8000000000000000) - 1
        
        y = self.X()
        assert y.value == 0
        y.copy_from(x)
        assert y.value == -(0x8000000000000000)
    
    def test_codec(self):
        x = self.X()

        x.value = 8
        assert str(x) == "value: 8\n"
        
        x.value = 1
        assert x.encode(">") == "\x00\x00\x00\x00\x00\x00\x00\x01"
        x.value = -1
        assert x.encode(">") == "\xff\xff\xff\xff\xff\xff\xff\xff"

        x.decode("\x00\x00\x00\x00\x00\x00\x00\x01", ">")
        assert x.value == 1
        x.decode("\xff\xff\xff\xff\xff\xff\xff\xff", ">")
        assert x.value == -1
        
        with pytest.raises(Exception):
            x.decode("\xff\xff\xff\xff\xff\xff\xff", ">")
        with pytest.raises(Exception):
            x.decode("\xff\xff\xff\xff\xff\xff\xff\xff\xff", ">")

class TestU8():

    class X(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.u8)]
    
    def test(self):
        x = self.X()
        assert x.value == 0
        x.value = 0
        assert x.value == 0
        x.value = 0xFF
        assert x.value == 0xFF
        
        with pytest.raises(Exception):
            x.value = "123"
        with pytest.raises(Exception):
            x.value = -1
        with pytest.raises(Exception):
            x.value = 0xFF + 1
        
        y = self.X()
        assert y.value == 0
        y.copy_from(x)
        assert y.value == 0xFF
    
    def test_codec(self):
        x = self.X()

        x.value = 5
        assert str(x) == "value: 5\n"
        
        assert x.encode(">") == "\x05"
        
        x.decode("\x05", ">")
        assert x.value == 5
        
        with pytest.raises(Exception):
            x.decode("", ">")
        with pytest.raises(Exception):
            x.decode("\xff\xff", ">")

class TestU16():

    class X(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.u16)]
    
    def test(self):
        x = self.X()
        assert x.value == 0
        x.value = 0
        assert x.value == 0
        x.value = 0xFFFF
        assert x.value == 0xFFFF
        
        with pytest.raises(Exception):
            x.value = "123"
        with pytest.raises(Exception):
            x.value = -1
        with pytest.raises(Exception):
            x.value = 0xFFFF + 1
        
        y = self.X()
        assert y.value == 0
        y.copy_from(x)
        assert y.value == 0xFFFF
    
    def test_codec(self):
        x = self.X()

        x.value = 5
        assert str(x) == "value: 5\n"
        
        assert x.encode(">") == "\x00\x05"
        
        x.decode("\x00\x05", ">")
        assert x.value == 5
        
        with pytest.raises(Exception):
            x.decode("\x00", ">")
        with pytest.raises(Exception):
            x.decode("\x00\xff\xff", ">")
            
class TestU32():

    class X(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.u32)]
    
    def test(self):
        x = self.X()
        assert x.value == 0
        x.value = 0
        assert x.value == 0
        x.value = 0xFFFFFFFF
        assert x.value == 0xFFFFFFFF
        
        with pytest.raises(Exception):
            x.value = "123"
        with pytest.raises(Exception):
            x.value = -1
        with pytest.raises(Exception):
            x.value = 0xFFFFFFFF + 1
        
        y = self.X()
        assert y.value == 0
        y.copy_from(x)
        assert y.value == 0xFFFFFFFF
    
    def test_codec(self):
        x = self.X()

        x.value = 5
        assert str(x) == "value: 5\n"
        
        assert x.encode(">") == "\x00\x00\x00\x05"
        
        x.decode("\x00\x00\x00\x05", ">")
        assert x.value == 5
        
        with pytest.raises(Exception):
            x.decode("\x00\x00\x00", ">")
        with pytest.raises(Exception):
            x.decode("\xff\xff\x00\x00\x00", ">")
            
class TestU64():

    class X(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.u64)]
    
    def test(self):
        x = self.X()
        assert x.value == 0
        x.value = 0
        assert x.value == 0
        x.value = 0xFFFFFFFFFFFFFFFF
        assert x.value == 0xFFFFFFFFFFFFFFFF
        
        with pytest.raises(Exception):
            x.value = "123"
        with pytest.raises(Exception):
            x.value = -1
        with pytest.raises(Exception):
            x.value = 0xFFFFFFFFFFFFFFFF + 1
        
        y = self.X()
        assert y.value == 0
        y.copy_from(x)
        assert y.value == 0xFFFFFFFFFFFFFFFF
    
    def test_codec(self):
        x = self.X()

        x.value = 5
        assert str(x) == "value: 5\n"
        
        assert x.encode(">") == "\x00\x00\x00\x00\x00\x00\x00\x05"
        
        x.decode("\x00\x00\x00\x00\x00\x00\x00\x05", ">")
        assert x.value == 5
        
        with pytest.raises(Exception):
            x.decode("\x00\x00\x00\x00\x00\x00\x05", ">")
        with pytest.raises(Exception):
            x.decode("\x00\x00\x00\x00\x00\x00\x00\x00\x05", ">")
