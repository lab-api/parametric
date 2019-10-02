from parametric import Parameter
import pytest

x = Parameter('x', 2, bounds=(2,4))
y = Parameter('y', 3)

def test_neg():
    assert -x == -2

def test_add():
    assert x + 2 == 2 + x == 4
    assert x + y == y + x == 5

def test_sub():
    assert x - 2 == -(2 - x) == 0
    assert x - y == -(y-x) == -1

def test_mult():
    assert 2*x == x*2 == 4
    assert x*y == y*x == 6

def test_div():
    assert x/2 == 1/(2/x) == 1
    assert x/y == 1/(y/x) == 2/3

def test_pow():
    assert x**2 == 2**x == 4
    assert x**y == 8

def test_ineq():
    assert y > x
    assert y >= x
    assert x < y
    assert x <= y

def test_inplace():
    z = Parameter('z', 1)

    z += 1
    assert z == 2

    z -= 1
    assert z == 1

    z *= 2
    assert z == 2

    z /= 2
    assert z == 1
    
def test_bounds():
    x.bounds = (0, 1)
    with pytest.raises(ValueError):
        assert x(-1)
    with pytest.raises(ValueError):
        assert x(2)
