import prophy
import pytest

def test_int_attributes():
    assert 1 == prophy.i8._SIZE
    assert False == prophy.i8._DYNAMIC
    assert False == prophy.i8._UNLIMITED
    assert 0 == prophy.i8._DEFAULT

    assert 2 == prophy.i16._SIZE
    assert False == prophy.i16._DYNAMIC
    assert False == prophy.i16._UNLIMITED
    assert 0 == prophy.i16._DEFAULT

    assert 4 == prophy.i32._SIZE
    assert False == prophy.i32._DYNAMIC
    assert False == prophy.i32._UNLIMITED
    assert 0 == prophy.i32._DEFAULT

    assert 8 == prophy.i64._SIZE
    assert False == prophy.i64._DYNAMIC
    assert False == prophy.i64._UNLIMITED
    assert 0 == prophy.i64._DEFAULT

    assert 1 == prophy.u8._SIZE
    assert False == prophy.u8._DYNAMIC
    assert False == prophy.u8._UNLIMITED
    assert 0 == prophy.u8._DEFAULT

    assert 2 == prophy.u16._SIZE
    assert False == prophy.u16._DYNAMIC
    assert False == prophy.u16._UNLIMITED
    assert 0 == prophy.u16._DEFAULT

    assert 4 == prophy.u32._SIZE
    assert False == prophy.u32._DYNAMIC
    assert False == prophy.u32._UNLIMITED
    assert 0 == prophy.u32._DEFAULT

    assert 8 == prophy.u64._SIZE
    assert False == prophy.u64._DYNAMIC
    assert False == prophy.u64._UNLIMITED
    assert 0 == prophy.u64._DEFAULT

def test_float_attributes():
    assert 4 == prophy.r32._SIZE
    assert False == prophy.r32._DYNAMIC
    assert False == prophy.r32._UNLIMITED
    assert 0 == prophy.r32._DEFAULT

    assert 8 == prophy.r64._SIZE
    assert False == prophy.r64._DYNAMIC
    assert False == prophy.r64._UNLIMITED
    assert 0 == prophy.r64._DEFAULT

def test_bytes_static_attributes():
    B = prophy.bytes(size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '\x00\x00\x00' == B._DEFAULT

def test_bytes_limited_attributes():
    B = prophy.bytes(bound = "a_len", size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '' == B._DEFAULT

def test_bytes_bound_attributes():
    B = prophy.bytes(bound = "a_len")

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert False == B._UNLIMITED
    assert '' == B._DEFAULT

def test_bytes_greedy_attributes():
    B = prophy.bytes()

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert True == B._UNLIMITED
    assert '' == B._DEFAULT
