from ..abc import NamdObject

def test_names():
    class Thing(NamdObject):
        pass

    assert str(Thing()) ==  'Thing'
    assert str(Thing('ABC')) == 'Thing ABC'