from simplify import simplify
import pytest


@pytest.fixture
def Simplified():
    @simplify
    class Simplified:
        def __init__(self, fst): pass

    return Simplified

@pytest.fixture
def SimplifiedOneDefaultArg():
    @simplify
    class Simplified:
        def __init__(self, fst=5): pass

    return Simplified

@pytest.fixture
def SimplifiedTwoArgs():
    @simplify
    class Simplified:
        def __init__(self, fst, snd): pass

    return Simplified

def test_no_args_in_init():
    @simplify
    class Simplified:
        def __init__(self): pass

    a = Simplified()
    assert len(a.__dict__) == 0

def test_two_args_in_init(SimplifiedTwoArgs):
    a = SimplifiedTwoArgs(5, 10)
    assert a.fst == 5
    assert a.snd == 10

def test_wrong_args_number(Simplified):
    with pytest.raises(TypeError):
        SimplifiedTwoArgs(5, 10)

def test_lt(SimplifiedTwoArgs):
    a = SimplifiedTwoArgs(1, 1)
    b = SimplifiedTwoArgs(1, 2)
    c = SimplifiedTwoArgs(2, 1)

    assert a < b
    assert a < c
    assert not c < a

def test_eq(SimplifiedTwoArgs):
    a = SimplifiedTwoArgs(1, 1)
    b = SimplifiedTwoArgs(1, 1)
    c = SimplifiedTwoArgs(1, 2)

    assert a == b
    assert not a == c

def test_overwritten_lt():
    @simplify
    class Simplified:
        def __init__(self, fst, snd): pass

        def __lt__(self, other):
            return False

    a = Simplified(1, 2)
    b = Simplified(2, 1)

    assert not a < b

def test_overwritten_eq():
    @simplify
    class Simplified:
        def __init__(self, fst, snd): pass

        def __eq__(self, other):
            return False

    a = Simplified(1, 1)
    b = Simplified(1, 1)

    assert not a == b

def test_str(SimplifiedTwoArgs):
    a = SimplifiedTwoArgs(1, 2)
    assert a.__str__() == '<Simplified (fst:1, snd:2)>'

def test_repr(SimplifiedTwoArgs):
    a = SimplifiedTwoArgs(1, 2)
    assert a.__repr__() == '<Simplified (fst:1, snd:2)>'

def test_overwritten_str():
    @simplify
    class Simplified:
        def __init__(self, fst, snd): pass

        def __str__(self):
            return 'My own str'

    a = Simplified(1, 2)
    assert a.__str__() == 'My own str'

def test_overwritten_repr():
    @simplify
    class Simplified:
        def __init__(self, fst, snd): pass

        def __str__(self):
            return 'My own repr'

    a = Simplified(1, 2)
    assert a.__repr__() == 'My own repr'

def test_simple_inheritance(Simplified):
    @simplify
    class SubSimplified(Simplified):
        def __init__(self, snd):
            super().__init__(snd * 2)

    b = SubSimplified(5)
    assert b.fst == 10
    assert b.snd == 5

def test_default_arguments_no_args(SimplifiedOneDefaultArg):
    a = SimplifiedOneDefaultArg()
    assert a.fst == 5

def test_default_arguments_one_pos_arg(SimplifiedOneDefaultArg):
    a = SimplifiedOneDefaultArg(10)
    assert a.fst == 10

def test_default_arguments_one_keyword_arg(SimplifiedOneDefaultArg):
    a = SimplifiedOneDefaultArg(fst=10)
    assert a.fst == 10

def test_wrong_keyword_used(SimplifiedOneDefaultArg):
    with pytest.raises(TypeError):
        SimplifiedOneDefaultArg(snd=5)

def test_no_default_args_use_keywords(SimplifiedTwoArgs):
    a = SimplifiedTwoArgs(fst=5, snd=10)
    assert a.fst == 5
    assert a.snd == 10

def test_no_default_args_use_keywords_reversed_order(SimplifiedTwoArgs):
    a = SimplifiedTwoArgs(snd=10, fst=5)
    assert a.fst == 5
    assert a.snd == 10

def test_no_default_args_use_mixed(SimplifiedTwoArgs):
    a = SimplifiedTwoArgs(5, snd=10)
    assert a.fst == 5
    assert a.snd == 10

def call_instance_method():
    @simplify
    class Simplified:
        def __init__(self, fst): pass

        def instance_method(self):
            return self.fst

    a = Simplified(5)
    assert a.instance_method() == 5

def call_static_method():
    @simplify
    class Simplified:
        a = 5

        def __init__(self): pass

        @staticmethod
        def static_method():
            return Simplified.a

    assert Simplified.static_method() == 5
    assert Simplified().static_method() == 5

def call_class_method():
    @simplify
    class Simplified:
        a = 5

        def __init__(self): pass

        @classmethod
        def class_method(cls):
            return cls.a

    assert Simplified.class_method() == 5
    assert Simplified().class_method() == 5
