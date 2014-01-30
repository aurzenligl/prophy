import aprot
import pytest

class Enumeration(aprot.enum):
    __metaclass__ = aprot.enum_generator
    _enumerators = [("Enumeration_One", 1),
                    ("Enumeration_Two", 2),
                    ("Enumeration_Three", 3)]

class Enumeration8(aprot.enum8):
    __metaclass__ = aprot.enum_generator
    _enumerators = Enumeration._enumerators

class TestEnum():
    
    class Enum(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", Enumeration)]
            
    def test_assignment(self):
        x = self.Enum()
        assert x.value == "Enumeration_One"
        x.value = "Enumeration_Two"
        assert x.value == "Enumeration_Two"
        x.value = 3
        assert x.value == "Enumeration_Three"
    
        with pytest.raises(Exception):
            x.value = "Enumeration_Four"
        with pytest.raises(Exception):
            x.value = 4
            
        y = self.Enum()
        assert y.value == "Enumeration_One"
        y.copy_from(x)
        assert y.value == "Enumeration_Three"
            
    def test_print(self):
        x = self.Enum()
        x.value = 2
        assert str(x) == "value: Enumeration_Two\n"
        
    def test_encode(self):
        x = self.Enum()
        x.value = 2
        assert x.encode(">") == "\x00\x00\x00\x02"
    
    def test_decode(self):
        x = self.Enum()
        x.decode("\x00\x00\x00\x02", ">") 
        assert x.value == "Enumeration_Two"
        
        with pytest.raises(Exception):
            x.decode("\x00\x00\x00\x09", ">")
        with pytest.raises(Exception):
            x.decode("\x00\x00\x01", ">")
        with pytest.raises(Exception):
            x.decode("\x00\x00\x00\x00\x01", ">")
            
    def test_exceptions(self):
        with pytest.raises(Exception):
            class NoEnumerators(aprot.enum):
                __metaclass__ = aprot.enum_generator
        with pytest.raises(Exception):
            class NamesOverlapping(aprot.enum):
                __metaclass__ = aprot.enum_generator
                _enumerators = [("NamesOverlapping_Overlap", 1),
                                ("NamesOverlapping_Overlap", 2)]
        with pytest.raises(Exception):
            class ValuesOverlapping(aprot.enum):
                __metaclass__ = aprot.enum_generator
                _enumerators = [("ValuesOverlapping_First", 42),
                                ("ValuesOverlapping_Second", 42)]
        with pytest.raises(Exception):
            class ValueOutOfBounds(aprot.enum):
                __metaclass__ = aprot.enum_generator
                _enumerators = [("OutOfBounds", 0xFFFFFFFF + 1)]

class TestEnum8():
    
    class Enum(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", Enumeration8)]
            
    def test_assignment(self):
        x = self.Enum()
        assert x.value == "Enumeration_One"
        x.value = "Enumeration_Two"
        assert x.value == "Enumeration_Two"
        x.value = 3
        assert x.value == "Enumeration_Three"
    
        with pytest.raises(Exception):
            x.value = "Enumeration_Four"
        with pytest.raises(Exception):
            x.value = 4
            
        y = self.Enum()
        assert y.value == "Enumeration_One"
        y.copy_from(x)
        assert y.value == "Enumeration_Three"
            
    def test_print(self):
        x = self.Enum()
        x.value = 2
        assert str(x) == "value: Enumeration_Two\n"
        
    def test_encode(self):
        x = self.Enum()
        x.value = 2
        assert x.encode(">") == "\x02"
    
    def test_decode(self):
        x = self.Enum()
        x.decode("\x02", ">")
        assert x.value == "Enumeration_Two"
        
        with pytest.raises(Exception):
            x.decode("\x09", ">")
        with pytest.raises(Exception):
            x.decode("", ">")
        with pytest.raises(Exception):
            x.decode("\x00\x01", ">")
            
    def test_exceptions(self):
        with pytest.raises(Exception):
            class NoEnumerators(aprot.enum8):
                __metaclass__ = aprot.enum_generator
        with pytest.raises(Exception):
            class NamesOverlapping(aprot.enum8):
                __metaclass__ = aprot.enum_generator
                _enumerators = [("NamesOverlapping_Overlap", 1),
                                ("NamesOverlapping_Overlap", 2)]
        with pytest.raises(Exception):
            class ValuesOverlapping(aprot.enum8):
                __metaclass__ = aprot.enum_generator
                _enumerators = [("ValuesOverlapping_First", 42),
                                ("ValuesOverlapping_Second", 42)]
        with pytest.raises(Exception):
            class ValueOutOfBounds(aprot.enum8):
                __metaclass__ = aprot.enum_generator
                _enumerators = [("OutOfBounds", -1)]

class TestEnumFixedArray():

    class Enum(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value", aprot.array(Enumeration, size = 2))]
    
    def test_assignment(self):
        x = self.Enum()
        assert x.value[:] == ["Enumeration_One", "Enumeration_One"]
        assert x.value[0] == "Enumeration_One"
        assert x.value[1] == "Enumeration_One"
        x.value[0] = 2
        x.value[1] = "Enumeration_Two"
        assert x.value[:] == ["Enumeration_Two", "Enumeration_Two"]
        
        y = self.Enum()
        assert y.value[:] == ["Enumeration_One", "Enumeration_One"]
        y.copy_from(x)
        assert y.value[:] == ["Enumeration_Two", "Enumeration_Two"]
    
    def test_print(self):
        x = self.Enum()
        x.value[:] = [2,2]
        assert str(x) == ("value: Enumeration_Two\n"
                          "value: Enumeration_Two\n")
        
    def test_encode(self):
        x = self.Enum()
        x.value[:] = [2,2]
        assert x.encode(">") == "\x00\x00\x00\x02\x00\x00\x00\x02"
    
    def test_decode(self):
        x = self.Enum()
        x.decode("\x00\x00\x00\x02\x00\x00\x00\x02", ">")
        assert x.value[0] == "Enumeration_Two"
        assert x.value[1] == "Enumeration_Two"
    
class TestEnumBoundArray():
    
    class Enum(aprot.struct):
        __metaclass__ = aprot.struct_generator
        _descriptor = [("value_len", aprot.u32),
                       ("value", aprot.array(Enumeration, bound = "value_len"))]
    
    def test_assignment(self):
        x = self.Enum()
        assert x.value[:] == []
        x.value[:] = [1, "Enumeration_One"]
        assert x.value[:] == ["Enumeration_One", "Enumeration_One"]
        assert x.value[0] == "Enumeration_One"
        assert x.value[1] == "Enumeration_One"
        x.value[0] = 2
        x.value[1] = "Enumeration_Two"
        assert x.value[:] == ["Enumeration_Two", "Enumeration_Two"]
    
    def test_print(self):
        x = self.Enum()
        x.value[:] = [2,2]
        assert str(x) == ("value: Enumeration_Two\n"
                          "value: Enumeration_Two\n")
        
    def test_encode(self):
        x = self.Enum()
        x.value[:] = [2,2]
        assert x.encode(">") == "\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02"
    
    def test_decode(self):
        x = self.Enum()
        x.decode("\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x02", ">")
        assert x.value[0] == "Enumeration_Two"
        assert x.value[1] == "Enumeration_Two"
        