from decor import simplify
import pytest

def test_no_args_in_init():
    @simplify
    class A:
        def __init__(self): pass

    a = A()
    assert len(a.__dict__) == 0

def test_two_args_in_init():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

    a = A(5, 10)
    assert a.fst == 5
    assert a.snd == 10

def test_wrong_args_number():
    @simplify
    class A:
        def __init__(self, fst): pass

    with pytest.raises(TypeError):
        A(5, 10)

def test_lt():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

    a = A(1, 1)
    b = A(1, 2)
    c = A(2, 1)

    assert a < b
    assert a < c
    assert not c < a

def test_eq():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

    a = A(1, 1)
    b = A(1, 1)
    c = A(1, 2)

    assert a == b
    assert not a == c

def test_overwritten_lt():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

        def __lt__(self, other):
            return False

    a = A(1, 2)
    b = A(2, 1)

    assert not a < b

def test_overwritten_eq():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

        def __eq__(self, other):
            return False

    a = A(1, 1)
    b = A(1, 1)

    assert not a == b

def test_str():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

    a = A(1, 2)
    assert a.__str__() == '<A (fst:1, snd:2)>'

def test_repr():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

    a = A(1, 2)
    assert a.__repr__() == '<A (fst:1, snd:2)>'

def test_overwritten_str():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

        def __str__(self):
            return 'My own str'

    a = A(1, 2)
    assert a.__str__() == 'My own str'

def test_overwritten_repr():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

        def __str__(self):
            return 'My own repr'

    a = A(1, 2)
    assert a.__repr__() == 'My own repr'

def test_simple_inheritance():
    @simplify
    class A:
        def __init__(self, fst): pass

    @simplify
    class B(A):
        def __init__(self, snd):
            super(B, self).__init__(snd * 2)

    b = B(5)
    assert b.fst == 10
    assert b.snd == 5

def test_default_arguments_no_args():
    @simplify
    class A:
        def __init__(self, fst=5): pass

    a = A()
    assert a.fst == 5

def test_default_arguments_one_pos_arg():
    @simplify
    class A:
        def __init__(self, fst=5): pass

    a = A(10)
    assert a.fst == 10

def test_default_arguments_one_keyword_arg():
    @simplify
    class A:
        def __init__(self, fst=5): pass

    a = A(fst=10)
    assert a.fst == 10

def test_wrong_keyword_used():
    @simplify
    class A:
        def __init__(self, fst): pass

    with pytest.raises(TypeError):
        a = A(snd=5)

def test_no_default_args_use_keywords():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

    a = A(fst=5, snd=10)
    assert a.fst == 5
    assert a.snd == 10

def test_no_default_args_use_keywords_reversed_order():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

    a = A(snd=10, fst=5)
    assert a.fst == 5
    assert a.snd == 10

def test_no_default_args_use_mixed():
    @simplify
    class A:
        def __init__(self, fst, snd): pass

    a = A(5, snd=10)
    assert a.fst == 5
    assert a.snd == 10
