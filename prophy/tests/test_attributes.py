import prophy
import pytest

def test_bytes_static_attributes():
    B = prophy.bytes(size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED

def test_bytes_limited_attributes():
    B = prophy.bytes(bound = "a_len", size = 3)

    assert 3 == B._SIZE
    assert False == B._DYNAMIC
    assert False == B._UNLIMITED

def test_bytes_bound_attributes():
    B = prophy.bytes(bound = "a_len")

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert False == B._UNLIMITED

def test_bytes_greedy_attributes():
    B = prophy.bytes()

    assert 0 == B._SIZE
    assert True == B._DYNAMIC
    assert True == B._UNLIMITED
