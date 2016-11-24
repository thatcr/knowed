from ..base import NamdObject


def test_names():
    class Thing(NamdObject):
        pass

    assert str(Thing()) == 'Thing'
    assert str(Thing('ABC')) == 'Thing ABC'

    assert repr(Thing()) == __name__ + '.' + Thing.__name__ + '()'
    assert repr(Thing('ABC')) == __name__ + '.' + Thing.__name__ + "('ABC',)"
