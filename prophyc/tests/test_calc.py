import pytest
from prophyc import calc

def test_calc_numeric():
    assert calc.eval('10 + 2', {}) == 12
    assert calc.eval('10 - 2', {}) == 8
    assert calc.eval('10 * 2', {}) == 20
    assert calc.eval('10 / 2', {}) == 5
    assert calc.eval('10 << 2', {}) == 40
    assert calc.eval('10 >> 2', {}) == 2

def test_calc_parens():
    assert calc.eval('10 + 2 * 3', {}) == 16
    assert calc.eval('(10 + 2) * 3', {}) == 36

def test_calc_variables():
    assert calc.eval('a + b', {'a': 2, 'b': 3}) == 5

def test_calc_nested_variables():
    assert calc.eval('a', {'a': 'b', 'b': 'c', 'c': 9}) == 9

def test_calc_errors():
    with pytest.raises(calc.ParseError) as e:
        calc.eval('&', {})
    assert 'illegal' in str(e.value)

    with pytest.raises(calc.ParseError) as e:
        calc.eval('++', {})
    assert 'syntax' in str(e.value)

    with pytest.raises(calc.ParseError) as e:
        calc.eval('unknown', {})
    assert 'not found' in str(e.value)
