import pytest
from calculator.engine import evaluate, CalcError

def test_basic_ops():
    assert evaluate("1+2*3") == 7
    assert evaluate("(1+2)*3") == 9
    assert evaluate("7//2") == 3
    assert evaluate("7%2") == 1
    assert evaluate("2**3") == 8

def test_floats():
    assert evaluate("7/2") == 3.5
    assert evaluate("-3.5 + 2") == -1.5

def test_right_assoc_power():
    assert evaluate("2**3**2") == 512  # 2 ** (3 ** 2)

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate("1/0")

def test_invalid():
    with pytest.raises(CalcError):
        evaluate("import os")
    with pytest.raises(CalcError):
        evaluate("os.system('ls')")
    with pytest.raises(CalcError):
        evaluate("")
