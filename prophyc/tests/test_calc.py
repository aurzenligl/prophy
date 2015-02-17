from prophyc import calc

def test_calc_numeric():
    assert calc.eval('10 + 2', {}) == 12
    assert calc.eval('10 - 2', {}) == 8
    assert calc.eval('10 * 2', {}) == 20
    assert calc.eval('10 / 2', {}) == 5

# shifts

# parens

def test_calc_variables():
    assert calc.eval('a + b', {'a': 2, 'b': 3}) == 5

def test_calc_nested_variables():
    assert calc.eval('a', {'a': 'b', 'b': 'c', 'c': 9}) == 9

# illegal

# syntax

# lookup