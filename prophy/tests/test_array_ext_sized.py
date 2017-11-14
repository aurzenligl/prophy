import pytest

import prophy


@pytest.fixture(scope = 'session')
def ExtSizedArr():
    class ExtSizedArr(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("sz", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "sz")),
                       ("b", prophy.array(prophy.u8, bound = "sz")),
                       ("c", prophy.array(prophy.u16, bound = "sz"))]
    return ExtSizedArr


@pytest.fixture
def read_stdout_stderr(capsys):
    class Capture(object):
        def __enter__(self):
            capsys.readouterr()
            return self

        def __exit__(self, *_):
            self.out, self.err = capsys.readouterr()
    return Capture

@pytest.mark.parametrize('sizer_name, expected_sizer_name', [
    ("numOfFields", "numOfField"),
    ("numOfField", "numOfFields"),
    ("numOfany_other_name_will_be_forgotten_in_this_case", "numOfField"),
    ("numOfany_other_name_will_be_forgotten_in_this_case", "any_wrong_name_expected")])
def test_ext_sized_can_be_lenient(sizer_name, expected_sizer_name, read_stdout_stderr):

    with read_stdout_stderr() as capture:

        class IForgotS(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [(sizer_name, prophy.u8),
                           ("field", prophy.array(prophy.u8, bound=expected_sizer_name))]

    assert capture.err == ""
    assert capture.out == "Warning: Sizing member '{}' of container 'field' not "\
        "found in the object 'IForgotS'.\n Picking '{}' as the missing sizer instead.\n\n".format(expected_sizer_name,
                                                                                                  sizer_name)
    assert IForgotS().field._BOUND == sizer_name

def test_ext_sized_will_not_forgive_mistakes_with_many_arrays():
    with pytest.raises(prophy.ProphyError) as e:
        class K(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [
                ('numOfField', prophy.u8),
                ("field", prophy.array(prophy.u8, bound="numOfField")),
                ('numOfField2', prophy.u8),
                ("field2", prophy.array(prophy.u8, bound="numOfField2_incorrect"))]
    assert "Sizing member 'numOfField2_incorrect' of container 'field2' not found in the object 'K'" in str(e.value)

def test_ext_sized_wrong_sizer_type():
    with pytest.raises(prophy.ProphyError) as e:
        class K(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [
                ('numOfField', prophy.r32),
                ("field", prophy.array(prophy.u8, bound="numOfField"))]
    assert "array K.field must be bound to an unsigned integer" == str(e.value)

def test_ext_sized_scalar_array_assignment(ExtSizedArr):
    x = ExtSizedArr()
    assert x.a == []
    assert len(x.a) == 0

    x.a[:] = [1, 2]
    assert x.a[:] == [1, 2]

    x.a[:] = [6, 7]
    assert x.a == [6, 7]

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

def test_ext_sized_scalar_array_with_shift_exceptions():
    with pytest.raises(Exception) as e:
        class XS1(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("len", prophy.u8),
                           ("a", prophy.array(prophy.u8, bound = "len", shift = 2)),
                           ("b", prophy.array(prophy.u8, bound = "len"))]
    assert str(e.value) == "Different bound shifts are unsupported in externally sized arrays (XS1.b)"

    with pytest.raises(Exception) as e:
        class XS2(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
            _descriptor = [("len", prophy.u8),
                           ("a", prophy.array(prophy.u8, bound = "len")),
                           ("b", prophy.array(prophy.u8, bound = "len", shift = 2))]
    assert str(e.value) == "Different bound shifts are unsupported in externally sized arrays (XS2.b)"

def test_ext_sized_scalar_array_decoding_exceptions(ExtSizedArr):
    x = ExtSizedArr()
    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x10\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00", ">")
    assert 'too few bytes to decode integer' in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(b"\x01\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00", ">")
    assert 'not all bytes of ExtSizedArr read' in str(e.value)

def test_multiple_arrays_size_mismatch_during_encoding(ExtSizedArr):
    x = ExtSizedArr()
    x.b[:] = [1]

    with pytest.raises(prophy.ProphyError) as e:
        x.encode(">")
    assert 'Size mismatch of arrays in ExtSizedArr: a, b, c' in str(e.value)

    x.a[:] = [0, 0]
    x.c[:] = [0, 0]

    with pytest.raises(prophy.ProphyError) as e:
        x.encode(">")
    assert 'Size mismatch of arrays in ExtSizedArr: a, b, c' in str(e.value)


def test_ext_sized_scalar_array_copy_from(ExtSizedArr):
    x = ExtSizedArr()
    x.a[:] = [1, 2]
    y = ExtSizedArr()
    y.a[:] = [5, 6, 7]   # initial value to override

    y.copy_from(x)
    assert y.a == [1, 2]

def test_ext_sized_empty_decode_encode(ExtSizedArr):
    x = ExtSizedArr()
    assert len(x.a) == 0
    x.decode(b"\x00", ">")
    assert len(x.a) == 0

    assert b"\x00" == x.encode(">")

def test_ext_sized_scalar_array_print(ExtSizedArr):
    x = ExtSizedArr()
    x.a[:] = [1, 2]

    assert str(x) == ("a: 1\n"
                      "a: 2\n")

    x.c[:] = [3, 4, 0xDEAD]
    x.c[:] = [3, 4]

    assert str(x) == ("a: 1\n"
                      "a: 2\n"
                      "c: 3\n"
                      "c: 4\n")

def test_ext_sized_scalar_array_encoding_big_endian(ExtSizedArr):
    x = ExtSizedArr()
    x.a[:] = [1, 2]
    x.b[:] = [0, 0]
    x.c[:] = [3, 4, 0xDEAD]
    x.c[:] = [3, 4]

    assert x.encode(">") == (b"\x02"
                             b"\x01\x02"
                             b"\x00\x00"
                             b"\x00\x03\x00\x04")

def test_ext_sized_scalar_array_encoding_little_endian(ExtSizedArr):
    x = ExtSizedArr()
    x.a[:] = [1]
    x.b[:] = [2]
    x.c[:] = [3]

    assert x.encode("<") == (b"\x01"
                             b"\x01"
                             b"\x02"
                             b"\x03\x00")

def test_ext_sized_scalar_array_decoding_big_endian(ExtSizedArr):
    x = ExtSizedArr()
    x.decode(b"\x03\x01\x02\xff\x00\x00\x00\x00\x04\x00\x05\x00\x06", ">")

    assert x.a == [1, 2, 0xff]
    assert x.b == [0, 0, 0]
    assert x.c == [4, 5, 6]
    assert str(x) == ("a: 1\n"
                      "a: 2\n"
                      "a: 255\n"
                      "b: 0\n"
                      "b: 0\n"
                      "b: 0\n"
                      "c: 4\n"
                      "c: 5\n"
                      "c: 6\n")

def test_ext_sized_scalar_array_decoding_little_endian(ExtSizedArr):
    x = ExtSizedArr()
    x.decode(b"\x02\x01\x02\x03\x04\x05\x00\x06\x00", "<")

    assert x.a == [1, 2]
    assert x.b == [3, 4]
    assert x.c == [5, 6]
    assert str(x) == ("a: 1\n"
                      "a: 2\n"
                      "b: 3\n"
                      "b: 4\n"
                      "c: 5\n"
                      "c: 6\n")


def test_ext_sized_scalar_array_distant_sizer():
    class ExtSizedArrDist(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("sz", prophy.u8),
                       ("something", prophy.u32),
                       ("a", prophy.array(prophy.u8, bound = "sz")),
                       ("b", prophy.array(prophy.u8, bound = "sz"))]

    x = ExtSizedArrDist()
    x.decode(b"\x02\x00\x00\x00\xff\x01\x02\x03\x04", ">")

    assert x.something == 255
    assert x.a == [1, 2]
    assert x.b == [3, 4]
    assert str(x) == ("something: 255\n"
                      "a: 1\n"
                      "a: 2\n"
                      "b: 3\n"
                      "b: 4\n")

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

def test_multi_ext_sized_arrays_sets_interwined():
    class MultipleExtSizedArrSetsInterwined(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("sz_a", prophy.u8),
                       ("a1", prophy.array(prophy.u16, bound = "sz_a")),
                       ("sz_b", prophy.u16),
                       ("b1", prophy.array(prophy.u32, bound = "sz_b")),
                       ("b2", prophy.array(prophy.u8, bound = "sz_b")),
                       ("a2", prophy.array(prophy.u16, bound = "sz_a"))]

    x = MultipleExtSizedArrSetsInterwined()
    ref = (b"\x01"
           b"\x00\x01"
           b"\x00\x02"
           b"\x00\x00\x00\x02\x00\x00\x00\x03"
           b"\x04\x05"
           b"\x00\x06")

    x.decode(ref, ">")

    assert x.a1 == [1]
    assert x.b1 == [2, 3]
    assert x.b2 == [4, 5]
    assert x.a2 == [6]

    assert ref == x.encode(">")

def test_ext_sized_scalar_array_with_shift():

    class XS(prophy.with_metaclass(prophy.struct_generator, prophy.struct_packed)):
        _descriptor = [("len", prophy.u8),
                       ("a", prophy.array(prophy.u8, bound = "len", shift = 2)),
                       ("b", prophy.array(prophy.u8, bound = "len", shift = 2))]
    x = XS()
    x.a[:] = [1, 2, 3, 4]
    x.b[:] = [5, 6, 7, 8]

    assert x.encode(">") == b"\x06\x01\x02\x03\x04\x05\x06\x07\x08"

    x.decode(b"\x06\x01\x02\x03\x04\x05\x06\x07\x08", ">")
    assert x.a[:] == [1, 2, 3, 4]
    assert x.b[:] == [5, 6, 7, 8]
