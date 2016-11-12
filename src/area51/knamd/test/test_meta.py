from ..meta import KnamedClass
from collections.abc import MappingView

from pytest import raises

def test_meta_construction():
    class Thing(metaclass=KnamedClass):
        pass

    assert hasattr(Thing, '__cache__')
    assert type(Thing.__cache__) is dict
    # what's the right abc to check?
    # assert isinstance(Thing.__cache__, MappingView)

def test_instances():
    class Thing(metaclass=KnamedClass):
        def __init__(self, *args):
            self.args = args

    assert type(Thing('a')) is Thing
    assert type(Thing(123)) is Thing

    assert type(Thing('a').args) is tuple

    assert Thing('a') is Thing('a')
    assert Thing('a') is not Thing('b')

    assert Thing('a').args == ('a',)
    assert Thing('a', 123).args == ('a', 123)

