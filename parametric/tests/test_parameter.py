from parametric import Parameter
import pytest

x = Parameter('x', 2)
y = Parameter('y', 3)

def test_neg():
    z = -x
    assert z() == -2

def test_add():
    z = x + 2
    assert z() == 4

    w = x + y
    assert w() == 5

def test_sub():
    z = x - 2
    assert z() == 0

    w = x - y
    assert w() == -1

def test_mult():
    z = 2*x
    assert z() == 4

    z = x*3
    assert z() == 6

    z = x*y
    assert z() == 6

    z == y*x
    assert z() == 6

def test_div():
    z = x/2
    assert z() == 1

    z = 2/x
    assert z() == 1

    z = x/y
    assert z() == 2/3

    z = y/x
    assert z() == 3/2

def test_bounds():
    x.bounds = (0, 1)
    with pytest.raises(ValueError):
        assert x(-1)
    with pytest.raises(ValueError):
        assert x(2)
