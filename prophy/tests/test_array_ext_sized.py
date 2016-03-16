import prophy
import pytest
from binascii import hexlify

@pytest.fixture(scope = 'session')
def ExtSizedArr():
    class ExtSizedArr(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("sz", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "sz")),
                       ("b", prophy.array(prophy.u8, bound = "sz")),
                       ("c", prophy.array(prophy.u16, bound = "sz"))]
    return ExtSizedArr

def format_bin_str(binstr):
    hx = hexlify(binstr)
    spl = [hx[i:i+2] for i in range(0, len(hx), 2)]
    return r'b"\x' + r'\x'.join(spl) + r'"'
    

def test_ext_sized_scalar_array_assignment(ExtSizedArr):
    x = ExtSizedArr()
    assert x.a == []
    assert x.a[:] == []
    assert len(x.a) == 0
    
    x.a[:] = [1, 2]
    assert x.a[:] == [1, 2]

    x.a[:] = [6, 7]
    assert x.a == [6, 7]
    assert x.a[:] == [6, 7]

    del x.a[1]
    assert x.a[:] == [6]

    with pytest.raises(Exception):
        x.a.len
    with pytest.raises(Exception):
        x.a.len = 10
    with pytest.raises(Exception):
        x.a = 10
    with pytest.raises(Exception):
        x.a[0] = "will fail type check"
    with pytest.raises(Exception):
        x.a[0] = -1
    with pytest.raises(Exception):
        x.a[:] = [1, 2, "abc"]

def test_ext_sized_scalar_array_copy_from(ExtSizedArr):
    x = ExtSizedArr()
    x.a[:] = [1, 2]
    y = ExtSizedArr()
    y.a[:] = [5, 6, 7] # initial value to override

    y.copy_from(x)
    assert y.a[:] == [1, 2]


def test_ext_sized_empty_decode(ExtSizedArr):
    x = ExtSizedArr()
    assert len(x.a) == 0
    x.decode(b"\x00", ">")
    assert len(x.a) == 0
    
def test_ext_sized_scalar_array_encoding(ExtSizedArr):
    x = ExtSizedArr()
    x.a[:] = [1, 2]

    assert x.encode(">") == b"\x02\x01\x02"
    assert str(x) == ("a: 1\n"
                      "a: 2\n")
    
    x.b[:] = [3, 4]

    assert x.encode(">") == b"\x02\x01\x02\x03\x04"

    print str(x)
    assert str(x) == ("a: 1\n"
                      "a: 2\n"
                      "b: 3\n"
                      "b: 4\n")
    
    x.decode(b"\x03\x01\x02\xff\x00\x00\x00\x00\x04\x00\x05\x00\x06", ">")
    assert x.a[:] == [1, 2, 0xff]
    assert x.c[:] == [4, 5, 6]

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x10\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00", ">")
    assert 'too few bytes to decode integer' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x01\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00", ">")
    assert 'not all bytes read' in str(e.value)

def test_ext_sized_scalar_array_exceptions():
    with pytest.raises(Exception):
        class LengthFieldNonexistent(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a", prophy.array(prophy.i32, bound = "nonexistent"))]
    with pytest.raises(Exception):
        class LengthFieldAfter(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a", prophy.array(prophy.i32, bound = "after")),
                           ("after", prophy.i32)]
    with pytest.raises(Exception):
        class LengthFieldIsNotAnInteger(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("not_an_int", "not_an_int"),
                           ("a", prophy.array(prophy.i32, bound = "not_an_int"))]
    assert 0 # TODO: test not implemented at all

def test_ext_sized_scalar_array_twice_in_struct():
    class X2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("b_len", prophy.u8),
                       ("a_len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "a_len")),
                       ("b", prophy.array(prophy.u8, bound = "b_len"))]

    x = X2()

    x.a[:] = [1, 2, 3]
    x.b[:] = [6, 7]
    assert b"\x02\x03\x01\x02\x03\x06\x07" == x.encode(">")

    x.decode(b"\x01\x02\x07\x08\x01", ">")
    assert [7, 8] == x.a[:]
    assert [1] == x.b[:]

def test_ext_sized_array_encode_1(ExtSizedArr):
    c = ExtSizedArr()
    c.a[:] = [1,2,3]
    c.b[:] = [4,5,6]
    c.c[:] = [7,8,9]
    
    st = c.encode("<")
    
    assert b"\x03\x01\x02\x03\x04\x05\x06\x07\x00\x08\x00\x09\x00" == st
    assert str(c) == """\
a: 1
a: 2
a: 3
b: 4
b: 5
b: 6
c: 7
c: 8
c: 9
"""

def test_ext_sized_array_encode_2(ExtSizedArr):
    c = ExtSizedArr()
    c.a[:] = [1,2]
    c.b[:] = [3,4]
    c.c[:] = [5,6]
    
    ref = b"\x02\x01\x02\x03\x04\x00\x05\x00\x06"
    assert ref == c.encode(">")
    
    d = ExtSizedArr()
    d.decode(ref,">")
    
    assert d.a == c.a
    assert d.b == d.b
    assert d.c == d.c
    

def test_ext_sized_array_exceeded_encode_1(ExtSizedArr):
    c = ExtSizedArr()
    c.a[:] = [1,2,3]
    c.b[:] = [4,5]
    c.c[:] = [6]

    assert c.a == [1,0,0]
    assert c.b == [4,5,0]
    assert c.c == [6,0,0]

    assert str(c) == """\
a: 1
a: 2
a: 3
b: 4
b: 5
b: 0
c: 6
c: 0
c: 0
"""
    st = c.encode(">")
    ref = b"\x03\x01\x02\x03\x04\x05\x00\x00\x06\x00\x00\x00\x00"
    assert ref == st

def test_ext_sized_array_exceeded_encode_2(ExtSizedArr):
    c = ExtSizedArr()
    c.a[:] = [1]
    c.b[:] = [2,3]
    c.c[:] = [4,5,6]
    
    assert c.a == [1,0,0]
    assert c.b == [2,3,0]
    assert c.c == [4,5,6]

    assert str(c) == """\
a: 1
a: 0
a: 0
b: 2
b: 3
b: 0
c: 4
c: 5
c: 6
"""
    st = c.encode(">")
    ref = b"\x03\x01\x00\x00\x02\x03\x00\x00\x04\x00\x05\x00\x06"

    print format_bin_str(st)
    print format_bin_str(ref)
    assert ref == st

def test_ext_sized_scalar_array_with_shift():
    class XS(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "len", shift = 2))]

    x = XS()
    x.a[:] = [1, 2, 3, 4]

    assert x.encode(">") == b"\x06\x01\x02\x03\x04"

    x.decode(b"\x06\x01\x02\x03\x04", ">")
    assert x.a[:] == [1, 2, 3, 4]

    with pytest.raises(Exception) as e:
        x.decode(b"\x01", ">")
    assert str(e.value) == "decoded array length smaller than shift"

    with pytest.raises(Exception) as e:
        x.decode(b"\x05", ">")
    assert str(e.value) == "too few bytes to decode integer"

    with pytest.raises(Exception) as e:
        x.decode(b"\x02\x00", ">")
    assert str(e.value) == "not all bytes read"

def test_ext_sized_scalar_array_with_shift_exceptions():
    with pytest.raises(Exception) as e:
        class Array(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a_len", prophy.u8),
                           ("a", prophy.array(prophy.u8, shift = 2))]
    assert str(e.value) == "only shifting bound array implemented"
    with pytest.raises(Exception) as e:
        class Array(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a_len", prophy.u8),
                           ("a", prophy.array(prophy.u8, size = 1, shift = 2))]
    assert str(e.value) == "only shifting bound array implemented"
    with pytest.raises(Exception) as e:
        class Array(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("a_len", prophy.u8),
                           ("a", prophy.array(prophy.u8, bound = "a_len", size = 1, shift = 2))]
    assert str(e.value) == "only shifting bound array implemented"
