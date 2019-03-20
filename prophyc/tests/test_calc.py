import pytest
from prophyc import calc


def test_calc_numeric():
    assert calc.eval('10 + 2', {}) == 12
    assert calc.eval('10 - 2', {}) == 8
    assert calc.eval('10 * 2', {}) == 20
    assert calc.eval('10 / 2', {}) == 5
    assert calc.eval('10 << 2', {}) == 40
    assert calc.eval('10 >> 2', {}) == 2
    assert calc.eval('-10', {}) == -10
    assert calc.eval('\n-10\n', {}) == -10
    assert calc.eval('0x0', {}) == 0
    assert calc.eval('0x3', {}) == 3
    assert calc.eval('\n-0x1a\n', {}) == -26
    assert calc.eval('0x2 + 0x00ff', {}) == 257
    assert calc.eval('0x2 - 0xff', {}) == -253


def test_calc_parens():
    assert calc.eval('10 + 2 * 3', {}) == 16
    assert calc.eval('(10 + 2) * 3', {}) == 36


def test_calc_variables():
    assert calc.eval('a + b', {'a': 2, 'b': 3}) == 5


def test_calc_nested_variables():
    assert calc.eval('a', {'a': 'b', 'b': 'c', 'c': 9}) == 9


def test_calc_errors():
    with pytest.raises(calc.ParseError, match="illegal character &"):
        calc.eval('&', {})

    with pytest.raises(calc.ParseError, match=r"syntax error at '\+'"):
        calc.eval('++', {})

    with pytest.raises(calc.ParseError, match="numeric constant 'unknown' not found"):
        calc.eval('unknown', {})

    with pytest.raises(calc.ParseError, match="numeric constant 'x2' not found"):
        calc.eval('2 + x2', {})
