from pytest import fixture

@fixture
def add():
    from arithmetictest import add
    return add

@fixture
def substract():
    from arithmetictest import subtract
    return subtract

@fixture
def multiply():
    from arithmetictest import multiply
    return multiply

@fixture
def division():
    from arithmetictest import division
    return division

def test_add(add):
	assert add(1,2) == 3

def test_substract(substract):
	assert substract(2,1) == 1

def test_multiply(multiply):
	assert multiply(2,1) == 2

def test_division(division):
	assert division(2,1) == 2
