import aprot
import pytest

class TestFixedBytes():

    class Bytes(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.bytes(size = 5))]
        
    def test_assignment(self):
        x = self.Bytes()
        assert x.value == "\x00\x00\x00\x00\x00"
        x.value = "\x00\x00\x01"
        assert x.value == "\x00\x00\x01\x00\x00"
        x.value = "\x00\x00"
        assert x.value == "\x00\x00\x00\x00\x00"
        x.value = "bytes"
        assert x.value == "bytes"
        x.value = "bts"
        assert x.value == "bts\x00\x00"
        
        with pytest.raises(Exception):
            x.value = 3
        with pytest.raises(Exception):
            x.value = "123456"
        
        y = self.Bytes()
        assert y.value == "\x00\x00\x00\x00\x00"
        y.copy_from(x)
        assert y.value == "bts\x00\x00"
    
    def test_print(self):
        x = self.Bytes()
        x.value = "abc"
        assert str(x) == "value: \'abc\\x00\\x00\'\n"
        x.value = "\x00\x01"
        assert str(x) == "value: \'\\x00\\x01\\x00\\x00\\x00\'\n"
        x.value = "ab\x00"
        assert str(x) == "value: \'ab\\x00\\x00\\x00\'\n"
    
    def test_encode(self):
        x = self.Bytes()
        x.value = "abc"
        assert x.encode(">") == "abc\x00\x00"
        x.value = "\x01"
        assert x.encode(">") == "\x01\x00\x00\x00\x00"
    
    def test_decode(self):
        x = self.Bytes()
        x.decode("abc\x00\x00", ">")
        assert x.value == "abc\x00\x00"
        x.decode("\x01\x00\x00\x00\x00", ">")
        assert x.value == "\x01\x00\x00\x00\x00"
        
        with pytest.raises(Exception):
            x.decode("\x01\x00\x00\x00\x00\x00", ">")
        with pytest.raises(Exception):
            x.decode("\x01\x00\x00\x00", ">")

class TestTwoFixedBytes():

    class Bytes(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("x", aprot.bytes(size = 5)),
                       ("y", aprot.bytes(size = 5))]
            
    def test_encode(self):
        x = self.Bytes()
        x.x = "abcde"
        x.y = "fghij"
        assert str(x) == ("x: \'abcde\'\n"
                          "y: \'fghij\'\n")
        assert x.encode(">") == "abcdefghij"
    
    def test_decode(self):
        x = self.Bytes()
        x.decode("abcdefghij", ">")
        assert x.x == "abcde"
        assert x.y == "fghij"
        
class TestBoundBytes():

    class Bytes(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value_len", aprot.u32),
                       ("value", aprot.bytes(bound = "value_len"))]
            
    def test_assignment(self):
        x = self.Bytes()
        assert x.value == ""
        x.value = "\x00\x00\x01"
        assert x.value == "\x00\x00\x01"
        x.value = "\x00\x00"
        assert x.value == "\x00\x00"
        x.value = "bytes"
        assert x.value == "bytes"
        x.value = "bts"
        assert x.value == "bts"
        
        with pytest.raises(Exception):
            x.value = 3
        
        y = self.Bytes()
        assert y.value == ""
        y.copy_from(x)
        assert y.value == "bts"
    
    def test_print(self):
        x = self.Bytes()
        x.value = "abc"
        assert str(x) == "value: \'abc\'\n"
        x.value = "\x00\x01"
        assert str(x) == "value: \'\\x00\\x01\'\n"
        x.value = "ab\x00"
        assert str(x) == "value: \'ab\\x00\'\n"
    
    def test_encode(self):
        x = self.Bytes()
        x.value = "abc"
        assert x.encode(">") == "\x00\x00\x00\x03abc"
        x.value = "\x01"
        assert x.encode(">") == "\x00\x00\x00\x01\x01"
    
    def test_decode(self):
        x = self.Bytes()
        x.decode("\x00\x00\x00\x03abc", ">")
        assert x.value == "abc"
        x.decode("\x00\x00\x00\x01\x01", ">")
        assert x.value == "\x01"

class TestShiftBoundBytes():

    class Bytes(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value_len", aprot.u8),
                       ("value", aprot.bytes(bound = "value_len", shift = 2))]
            
    def test_encode(self):
        x = self.Bytes()
        x.value = "abc"
        assert x.encode(">") == "\x05abc"
        x.value = "\x01"
        assert x.encode(">") == "\x03\x01"
        
    def test_decode(self):
        x = self.Bytes()
        x.decode("\x05abc", ">")
        assert x.value == "abc"
        x.decode("\x03\x01", ">")
        assert x.value == "\x01"

        with pytest.raises(Exception) as e:
            x.decode("\x01", ">")
        assert e.value.message == "decoded array length smaller than shift"
        with pytest.raises(Exception) as e:
            x.decode("\x05", ">")
        assert e.value.message == "too few bytes to decode string"
        with pytest.raises(Exception) as e:
            x.decode("\x02\x00", ">")
        assert e.value.message == "not all bytes read"
        
    def test_exceptions(self):
        with pytest.raises(Exception) as e:
            class Bytes(aprot.struct):
                __metaclass__ = aprot.struct_generator
                _descriptor = [("value_len", aprot.u8),
                               ("value", aprot.bytes(shift = 2))]
        assert e.value.message == "only shifting bound bytes implemented"
        with pytest.raises(Exception) as e:
            class Bytes(aprot.struct):
                __metaclass__ = aprot.struct_generator
                _descriptor = [("value_len", aprot.u8),
                               ("value", aprot.bytes(size = 1, shift = 2))]
        assert e.value.message == "only shifting bound bytes implemented"
        with pytest.raises(Exception) as e:
            class Bytes(aprot.struct):
                __metaclass__ = aprot.struct_generator
                _descriptor = [("value_len", aprot.u8),
                               ("value", aprot.bytes(bound = "value_len", size = 1, shift = 2))]
        assert e.value.message == "only shifting bound bytes implemented"

class TestTwoBoundBytes():

    class Bytes(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("x_len", aprot.u32),
                       ("y_len", aprot.u32),
                       ("x", aprot.bytes(bound = "x_len")),
                       ("y", aprot.bytes(bound = "y_len"))]
        
    def test_encode(self):
        x = self.Bytes()
        x.x = "abcde"
        x.y = "fghij"
        assert str(x) == ("x: \'abcde\'\n"
                          "y: \'fghij\'\n")
        assert x.encode(">") == "\x00\x00\x00\x05\x00\x00\x00\x05abcdefghij"

    def test_decode(self):
        x = self.Bytes()
        x.decode("\x00\x00\x00\x05\x00\x00\x00\x05abcdefghij", ">")
        assert x.x == "abcde"
        assert x.y == "fghij"

class TestLimitedBytes():

    class Bytes(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value_len", aprot.u32),
                       ("value", aprot.bytes(size = 5, bound = "value_len"))]
            
    def test_assignment(self):
        x = self.Bytes()
        assert x.value == ""
        x.value = "\x00\x00\x01"
        assert x.value == "\x00\x00\x01"
        x.value = "\x00\x00"
        assert x.value == "\x00\x00"
        x.value = "bytes"
        assert x.value == "bytes"
        x.value = "bts"
        assert x.value == "bts"
        
        with pytest.raises(Exception):
            x.value = 3
        with pytest.raises(Exception):
            x.value = "123456"
        
        y = self.Bytes()
        assert y.value == ""
        y.copy_from(x)
        assert y.value == "bts"
    
    def test_print(self):
        x = self.Bytes()
        x.value = "abc"
        assert str(x) == "value: \'abc\'\n"
        x.value = "\x00\x01"
        assert str(x) == "value: \'\\x00\\x01\'\n"
        x.value = "ab\x00"
        assert str(x) == "value: \'ab\\x00\'\n"
    
    def test_encode(self):
        x = self.Bytes()
        x.value = "abc"
        assert x.encode(">") == "\x00\x00\x00\x03abc\x00\x00"
        x.value = "\x01"
        assert x.encode(">") == "\x00\x00\x00\x01\x01\x00\x00\x00\x00"
    
    def test_decode(self):
        x = self.Bytes()
        x.decode("\x00\x00\x00\x03abc\x00\x00", ">")
        assert x.value == "abc"
        x.decode("\x00\x00\x00\x01\x01\x00\x00\x00\x00", ">")
        assert x.value == "\x01"

class TestTwoLimitedBytes():

    class Bytes(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("x_len", aprot.u32),
                       ("y_len", aprot.u32),
                       ("x", aprot.bytes(size = 5, bound = "x_len")),
                       ("y", aprot.bytes(size = 5, bound = "y_len"))]
            
    def test_encode(self):
        x = self.Bytes()
        x.x = "abc"
        x.y = "fgh"
        assert str(x) == ("x: \'abc\'\n"
                          "y: \'fgh\'\n")
        assert x.encode(">") == "\x00\x00\x00\x03\x00\x00\x00\x03abc\x00\x00fgh\x00\x00"
    
    def test_decode(self):
        x = self.Bytes()
        x.decode("\x00\x00\x00\x03\x00\x00\x00\x03abc\x00\x00fgh\x00\x00", ">")
        assert x.x == "abc"
        assert x.y == "fgh"

class TestGreedyBytes():

    class Bytes(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.bytes())]
            
    def test_assignment(self):
        x = self.Bytes()
        assert x.value == ""
        x.value = "\x00\x00\x01"
        assert x.value == "\x00\x00\x01"
        x.value = "\x00\x00"
        assert x.value == "\x00\x00"
        x.value = "bytes"
        assert x.value == "bytes"
        x.value = "bts"
        assert x.value == "bts"

        with pytest.raises(Exception):
            x.value = 3
    
        y = self.Bytes()
        assert y.value == ""
        y.copy_from(x)
        assert y.value == "bts"
            
    def test_print(self):
        x = self.Bytes()
        x.value = "abc"
        assert str(x) == "value: \'abc\'\n"
        x.value = "\x00\x01"
        assert str(x) == "value: \'\\x00\\x01\'\n"
        x.value = "ab\x00"
        assert str(x) == "value: \'ab\\x00\'\n"
    
    def test_encode(self):
        x = self.Bytes()
        x.value = "abc"
        assert x.encode(">") == "abc"
        x.value = "\x01"
        assert x.encode(">") == "\x01"
    
    def test_decode(self):
        x = self.Bytes()
        x.decode("abc", ">")
        assert x.value == "abc"
        x.decode("\x01", ">")
        assert x.value == "\x01"
       
class TestLastGreedyBytes():
    
    class Bytes(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("x", aprot.u32),
                       ("y", aprot.bytes())]
            
    def test_encode(self):
        x = self.Bytes()
        x.x = 1
        x.y = "fgh"
        assert str(x) == ("x: 1\n"
                          "y: \'fgh\'\n")
        assert x.encode(">") == "\x00\x00\x00\x01fgh"
    
    def test_decode(self):
        x = self.Bytes()
        x.decode("\x00\x00\x00\x01fgh", ">")
        assert x.x == 1
        assert x.y == "fgh"

def test_greedy_bytes_not_last_exceptions():
    with pytest.raises(Exception):
        class LastGreedyBytes(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("x", aprot.bytes()),
                           ("y", aprot.u32)]
    with pytest.raises(Exception):
        class X(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("x", aprot.u32),
                           ("y", aprot.bytes())]
        class Y(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("x", X),
                           ("y", aprot.u32)]
    with pytest.raises(Exception):
        class X(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("x", aprot.u32),
                           ("y", aprot.bytes())]
        class Y(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("x", aprot.u32),
                           ("y", aprot.array(X, size = 2))]
    with pytest.raises(Exception):
        class X(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("x", aprot.u32),
                           ("y", aprot.bytes())]
        class Y(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("x", aprot.u32),
                           ("y", X)]
        class Z(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("x", Y),
                           ("y", X)]
            
def test_array_of_bytes_exceptions():
    with pytest.raises(Exception):
        class Bytes(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("value", aprot.array(aprot.bytes(size = 5), size = 5))]
    with pytest.raises(Exception):
        class Bytes(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("value_len", aprot.u32),
                           ("value", aprot.array(aprot.bytes(size = 5), bound = "value_len"))]
            
def test_greedy_bytes_in_array_exceptions():
    with pytest.raises(Exception):
        class X(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("x", aprot.array(aprot.bytes(size = 2), size = 2))]
    with pytest.raises(Exception):
        class X(aprot.struct):
            __metaclass__ = aprot.struct_generator
            _descriptor = [("z", aprot.u32),
                           ("y", aprot.u32),
                           ("x", aprot.array(aprot.bytes(bound = "y"), bound = "z"))]
            