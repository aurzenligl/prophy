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
    spl = [hx[i:i + 2] for i in range(0, len(hx), 2)]
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
    y.a[:] = [5, 6, 7]   # initial value to override

    y.copy_from(x)
    assert y.a[:] == [1, 2]


def test_ext_sized_empty_decode(ExtSizedArr):
    x = ExtSizedArr()
    assert len(x.a) == 0
    x.decode(b"\x00", ">")
    assert len(x.a) == 0

def test_ext_sized_scalar_array_print(ExtSizedArr):
    x = ExtSizedArr()
    x.a[:] = [1, 2]

    assert str(x) == ("a: 1\n"
                      "a: 2\n"
                      "b: 0\n"
                      "b: 0\n"
                      "c: 0\n"
                      "c: 0\n")
    
    x.c[:] = [3, 4, 0xDEAD]
    x.c[:] = [3, 4]
    
    assert str(x) == ("a: 1\n"
                      "a: 2\n"
                      "b: 0\n"
                      "b: 0\n"
                      "c: 3\n"
                      "c: 4\n")

def test_ext_sized_scalar_array_encoding(ExtSizedArr):
    x = ExtSizedArr()
    x.a[:] = [1, 2]

    assert x.encode(">") == b"\x02\x01\x02\x00\x00\x00\x00\x00\x00"

    x.c[:] = [3, 4, 5]
    x.c[:] = [3, 4]

    assert x.encode(">") == b"\x02\x01\x02\x00\x00\x00\x03\x00\x04"


def test_ext_sized_scalar_array_decoding(ExtSizedArr):
    
    x = ExtSizedArr()
    x.decode(b"\x03\x01\x02\xff\x00\x00\x00\x00\x04\x00\x05\x00\x06", ">")
    
    assert x.a[:] == [1, 2, 0xff]
    assert x.b[:] == [0, 0, 0]    
    assert x.c[:] == [4, 5, 6]
    
    assert str(x) == ("a: 1\n"
                      "a: 2\n"
                      "a: 255\n"
                      "b: 0\n"
                      "b: 0\n"
                      "b: 0\n"
                      "c: 4\n"
                      "c: 5\n"
                      "c: 6\n")

def test_ext_sized_scalar_array_distant_sizer(ExtSizedArr):
    class ExtSizedArrDist(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("sz", prophy.u8),
                       ("something", prophy.u32),
                       ("a", prophy.array(prophy.u8, bound = "sz")),
                       ("b", prophy.array(prophy.u8, bound = "sz")),
                       ("c", prophy.array(prophy.u16, bound = "sz"))]
        
    test_ext_sized_scalar_array_decoding(ExtSizedArrDist)
    test_ext_sized_scalar_array_encoding(ExtSizedArrDist)
    
def test_ext_sized_scalar_array_decoding_exceptions(ExtSizedArr):
    x = ExtSizedArr()
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
    c.a[:] = [1, 2, 3]
    c.b[:] = [4, 5, 6]
    c.c[:] = [7, 8, 9]

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
    c.a[:] = [1, 2]
    c.b[:] = [3, 4]
    c.c[:] = [5, 6]

    ref = b"\x02\x01\x02\x03\x04\x00\x05\x00\x06"
    assert ref == c.encode(">")

    d = ExtSizedArr()
    d.decode(ref, ">")

    assert d.a == c.a
    assert d.b == d.b
    assert d.c == d.c


def test_ext_sized_array_exceeded_print(ExtSizedArr):

    c = ExtSizedArr()
    c.a[:] = [1, 2, 3]
    c.b[:] = [4, 5]
    c.c[:] = [6]

    assert str(c) == "a: 1\na: 2\na: 3\nb: 4\nb: 5\nb: 0\nc: 6\nc: 0\nc: 0\n"

    assert c.a == [1, 2, 3]
    assert c.b == [4, 5]
    assert c.c == [6]

def test_ext_sized_array_exceeded_encode_1(ExtSizedArr):
    c = ExtSizedArr()
    c.a[:] = [1, 2, 3]
    c.b[:] = [4, 5]
    c.c[:] = [6]

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

    assert c.a == [1, 2, 3]
    assert c.b == [4, 5]
    assert c.c == [6]

    st = c.encode(">")
    ref = b"\x03\x01\x02\x03\x04\x05\x00\x00\x06\x00\x00\x00\x00"
    assert ref == st

def test_ext_sized_array_exceeded_encode_2(ExtSizedArr):
    c = ExtSizedArr()
    c.a[:] = [1]
    c.b[:] = [2, 3]
    c.c[:] = [4, 5, 0xDEAD]
    c.c[:] = [7, 8]

    assert c.a == [1]
    assert c.b == [2, 3]
    assert c.c == [7, 8]

    ref = b"\x02\x01\x00\x02\x03\x00\x07\x00\x08"
    assert ref == c.encode(">")

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
