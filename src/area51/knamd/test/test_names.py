from ..abc import KnamedObject

def test_names():
    class Thing(KnamedObject):
        pass

    assert str(Thing()) ==  'Thing'
    assert str(Thing('ABC')) == 'Thing ABC'