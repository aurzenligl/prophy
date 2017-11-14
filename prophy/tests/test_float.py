import prophy
import pytest

def Float():
    class Float(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("value", prophy.r32)]
    return Float

def Double():
    class Double(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [("value", prophy.r64)]
    return Double

@pytest.mark.parametrize("FloatTypeFactory", [Float, Double])
def test_float(FloatTypeFactory):
    FloatType = FloatTypeFactory()
    x = FloatType()
    assert x.value == 0.0

    x.value = 1.455
    assert x.value == 1.455

    with pytest.raises(Exception):
        x.value = b"45.486"

    y = FloatType()
    y.value = 4.1
    y.copy_from(x)
    assert y.value == 1.455

@pytest.mark.parametrize("FloatTypeFactory, one, minus_one, too_long, too_short", [
    (Float,
        b"\x3f\x80\x00\x00",
        b"\xbf\x80\x00\x00",
        b"\xff\xff\xff\xff\xff",
        b"\xff\xff\xff"),
    (Double,
        b"\x3f\xf0\x00\x00\x00\x00\x00\x00",
        b"\xbf\xf0\x00\x00\x00\x00\x00\x00",
        b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff",
        b"\xff\xff\xff\xff\xff")
])
def test_float_codec(FloatTypeFactory, one, minus_one, too_long, too_short):
    x = FloatTypeFactory()()

    x.value = 8
    assert str(x) == "value: 8\n"

    x.decode(one, ">")
    assert x.value == 1.0

    x.decode(minus_one, ">")
    assert x.value == -1.0

    x.value = 1.0
    assert x.encode(">") == one

    x.value = -1.0
    assert x.encode(">") == minus_one

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(too_long, ">")
    assert "not all bytes of {} read".format(FloatTypeFactory.__name__) in str(e.value)

    with pytest.raises(prophy.ProphyError) as e:
        x.decode(too_short, ">")
    assert "too few bytes to decode integer" in str(e.value)
