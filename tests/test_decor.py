from decor import simplify
import pytest

def test_no_args_in_init():
    @simplify
    class A:
        def __init__(self):
            pass

    a = A()
    assert len(a.__dict__) == 0

def test_two_args_in_init():
    @simplify
    class A:
        def __init__(self, fst, snd):
            pass

    a = A(5, 10)
    for arg, val in zip(('fst', 'snd'), (5, 10)):
        assert a.__dict__[arg] == val

def test_wrong_args_number():
    @simplify
    class A:
        def __init__(self, fst):
            pass

    with pytest.raises(Exception):
        A(5, 10)

def test_lt():
    @simplify
    class A:
        def __init__(self, fst, snd):
            pass

    a = A(1, 1)
    b = A(1, 2)
    c = A(2, 1)

    assert a < b
    assert a < c
    assert not c < a

def test_eq():
    @simplify
    class A:
        def __init__(self, fst, snd):
            pass

    a = A(1, 1)
    b = A(1, 1)
    c = A(1, 2)

    assert a == b
    assert not a == c

def test_overwritten_lt():
    @simplify
    class A:
        def __init__(self, fst, snd):
            pass

        def __lt__(self, other):
            return False

    a = A(1, 2)
    b = A(2, 1)

    assert not a < b

def test_overwritten_eq():
    @simplify
    class A:
        def __init__(self, fst, snd):
            pass

        def __eq__(self, other):
            return False

    a = A(1, 1)
    b = A(1, 1)

    assert not a == b

def test_str():
    @simplify
    class A:
        def __init__(self, fst, snd):
            pass

    a = A(1, 2)
    assert a.__str__() == '[fst:1, snd:2]'

def test_repr():
    @simplify
    class A:
        def __init__(self, fst, snd):
            pass

    a = A(1, 2)
    assert a.__repr__() == '[fst:1, snd:2]'

def test_overwritten_str():
    @simplify
    class A:
        def __init__(self, fst, snd):
            pass

        def __str__(self):
            return 'My own str'

    a = A(1, 2)
    assert a.__str__() == 'My own str'

def test_overwritten_repr():
    @simplify
    class A:
        def __init__(self, fst, snd):
            pass

        def __str__(self):
            return 'My own repr'

    a = A(1, 2)
    assert a.__repr__() == 'My own repr'
